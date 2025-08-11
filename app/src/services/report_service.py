from datetime import datetime
from io import BytesIO
import os
from pathlib import Path
import threading
import time
from typing import Any, Dict, List

import matplotlib
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

from app.src.repository import OrderRepository
from app.src.schemas.report_schema import OrderReport

matplotlib.use("Agg")


def _serialize_orders(orders: List[OrderReport]) -> List[Dict[str, Any]]:
    orders_data: List[Dict[str, Any]] = []
    for order in orders:
        order_dict = {
            "id": order.id,
            "created_at": (
                order.created_at.isoformat()
                if hasattr(order.created_at, "isoformat")
                else str(order.created_at)
            ),
            "is_ready": order.is_ready,
            "items": [
                {
                    "dish_name": item.dish_name,
                    "quantity": item.quantity,
                    "price": float(item.price),
                }
                for item in order.items
            ],
        }
        orders_data.append(order_dict)
    return orders_data


def _generate_pdf_sync(orders_data: List[Dict[str, Any]], reports_dir: str) -> str:
    """Синхронна генерація PDF"""
    time.sleep(3)
    buffer = BytesIO()
    pdf = Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    pdf.setFont("Times-Roman", 14)
    pdf.drawString(50, y, "Order Report for users orders")
    y -= 30

    total_sum = 0
    dish_popularity: Dict[str, int] = {}

    for order in orders_data:
        pdf.setFont("Times-Roman", 12)

        # Обробляємо дату
        created_at = order["created_at"]
        if isinstance(created_at, str):
            try:
                # Якщо це ISO формат
                dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                created_at = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                # Якщо не вдалося розпарсити, залишаємо як є
                pass

        is_ready = order["is_ready"]
        pdf.drawString(
            50,
            y,
            f"Order #{order['id']} — Created: {created_at} — "
            f"Ready: {'Yes' if is_ready else 'No'}",
        )
        y -= 20

        pdf.setFont("Times-Roman", 11)
        for item in order["items"]:
            item_total = item["quantity"] * item["price"]
            total_sum += item_total
            dish_popularity[item["dish_name"]] = (
                dish_popularity.get(item["dish_name"], 0) + item["quantity"]
            )

            pdf.drawString(
                70,
                y,
                f"{item['dish_name']} — {item['quantity']} pcs × "
                f"{item['price']:.2f} = {item_total:.2f} UAH",
            )
            y -= 15

            if y < 100:
                pdf.showPage()
                y = height - 50

        y -= 10

    pdf.setFont("Times-Roman", 12)
    pdf.drawString(50, y, f"Total: {total_sum:.2f} UAH")

    # Генерація графіка
    if dish_popularity:
        try:
            fig, ax = plt.subplots(figsize=(6, 3))
            dishes = list(dish_popularity.keys())
            quantities = list(dish_popularity.values())

            ax.bar(dishes, quantities, color="skyblue")
            ax.set_title("Most Popular Dishes")
            ax.set_ylabel("Quantity Ordered")
            plt.xticks(rotation=45, ha="right")
            fig.tight_layout()

            img_buf = BytesIO()
            plt.savefig(img_buf, format="PNG", dpi=100, bbox_inches="tight")
            plt.close(fig)
            img_buf.seek(0)

            pdf.showPage()
            pdf.drawImage(ImageReader(img_buf), x=50, y=200, width=500, height=250)
        except Exception as e:
            print(f"Error generating chart: {e}")

    pdf.save()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_report_{timestamp}.pdf"
    file_path = os.path.join(reports_dir, filename)

    with open(file_path, "wb") as f:
        f.write(buffer.getvalue())

    print(f"✅ Report saved at: {file_path}")
    return file_path


class ReportService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
        current_dir = Path(__file__).resolve()
        base_dir = current_dir.parents[3]
        self.reports_dir = base_dir / "reports"

    async def start_report_in_thread(self) -> None:
        max_connections = 5
        pool = threading.BoundedSemaphore(value=max_connections)
        orders = await self.all_orders_data()
        orders_data = _serialize_orders(orders)
        with pool:
            thr = threading.Thread(
                target=_generate_pdf_sync, args=(orders_data, self.reports_dir)
            )
            thr.start()

    # async def start_report_in_process(self) -> None:
    #     multiprocessing.set_start_method("spawn")
    #     orders = await self.all_orders_data()
    #     orders_data = _serialize_orders(orders)
    #
    #     p = Process(
    #         target=_generate_pdf_sync, args=(orders_data, self.reports_dir)
    #     )
    #     p.start()

    async def all_orders_data(self) -> List[OrderReport]:
        return await self.order_repository.get_all_orders_with_details()

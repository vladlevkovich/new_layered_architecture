from dependency_injector import containers, providers

from app.src.core import Database, config
from app.src.repository import (
    CartRepository,
    MenuRepository,
    OrderRepository,
    UserRepository,
)
from app.src.services import (
    CartService,
    EmailService,
    MenuService,
    NotificationService,
    OrderService,
    ReportService,
    UserService,
)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.src.api.user_routes",
            "app.src.api.menu_routes",
            "app.src.api.cart_routes",
            "app.src.api.order_routes",
            "app.src.api.report_routes",
        ]
    )

    container_config = providers.Configuration()

    # Email config
    smtp_host = providers.Object(config.SMTP_HOST)
    smtp_port = providers.Object(config.SMTP_PORT)
    smtp_user = providers.Object(config.EMAIL_HOST_USER)
    smtp_password = providers.Object(config.EMAIL_HOST_PASSWORD)

    # Database
    db = providers.Singleton(Database, db_url=config.DB_URL)
    session = providers.Resource(lambda db: db.db_session(), db=db)

    # Email service
    email_service = providers.Factory(
        EmailService,
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        smtp_user=smtp_user,
        smtp_password=smtp_password,
    )

    # Notification service
    notification_service = providers.Factory(
        NotificationService, email_service=email_service
    )

    # Repositories
    user_repository = providers.Factory(UserRepository, session=session)
    menu_repository = providers.Factory(MenuRepository, session=session)
    cart_repository = providers.Factory(CartRepository, session=session)
    order_repository = providers.Factory(
        OrderRepository, session=session, cart_repository=cart_repository
    )

    # Services
    user_service = providers.Factory(UserService, user_repository=user_repository)
    menu_service = providers.Factory(MenuService, menu_repository=menu_repository)
    cart_service = providers.Factory(CartService, cart_repository=cart_repository)
    order_service = providers.Factory(
        OrderService,
        order_repository=order_repository,
        notification_service=notification_service,
    )
    report_service = providers.Factory(ReportService, order_repository=order_repository)

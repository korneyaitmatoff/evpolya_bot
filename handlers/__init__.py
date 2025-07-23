from .get_service_callback import dp
from .handle_add_member import dp
from .handler_remove_member import dp
from .process_pre_checkout_query import dp
from .process_successful_payment import dp
from .process_unsuccessful_payment import dp
from .start import dp
from .start_subs_bot import dp

__all__ = ["dp"]

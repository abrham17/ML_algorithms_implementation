# Tool definitions for Gemini
# Tool definitions for Gemini
from api.models import Transaction, Inventory, CustomUser, Schedule

def log_transaction(product_name, quantity, price, transaction_type, user_id):
    """
    Logs a financial transaction (Sale or Purchase).
    """
    try:
        user = CustomUser.objects.get(id=user_id)
        # Find or create product (simplified logic)
        product, created = Inventory.objects.get_or_create(
            name__iexact=product_name,
            defaults={'name': product_name, 'unit_price': price, 'stock_quantity': 0}
        )
        
        # Update stock
        if transaction_type.upper() == 'SALE':
            product.stock_quantity -= int(quantity)
        else:
            product.stock_quantity += int(quantity)
        product.save()

        # Create record
        Transaction.objects.create(
            user=user,
            product=product,
            transaction_type=transaction_type.upper(),
            quantity=quantity,
            total_amount=float(price) * int(quantity)
        )
        return f"Successfully logged {transaction_type} of {quantity} {product_name}."
    except Exception as e:
        return f"Error logging transaction: {str(e)}"

from api.services.calendar import GoogleCalendarService
from api.services.market import MarketDataService

def log_transaction(product_name, quantity, price, transaction_type, user_id):
    """
    Logs a financial transaction (Sale or Purchase).
    """
    try:
        user = CustomUser.objects.get(id=user_id)
        # Find or create product (simplified logic)
        product, created = Inventory.objects.get_or_create(
            name__iexact=product_name,
            defaults={'name': product_name, 'unit_price': price, 'stock_quantity': 0}
        )
        
        # Update stock
        if transaction_type.upper() == 'SALE':
            product.stock_quantity -= int(quantity)
        else:
            product.stock_quantity += int(quantity)
        product.save()

        # Create record
        Transaction.objects.create(
            user=user,
            product=product,
            transaction_type=transaction_type.upper(),
            quantity=quantity,
            total_amount=float(price) * int(quantity)
        )
        return f"Successfully logged {transaction_type} of {quantity} {product_name}."
    except Exception as e:
        return f"Error logging transaction: {str(e)}"

def schedule_compliance_event(title, date_str, user_id):
    """
    Schedules a compliance event (e.g., Tax Payment) in the calendar.
    date_str format: YYYY-MM-DD
    """
    try:
        user = CustomUser.objects.get(id=user_id)
        service = GoogleCalendarService(user)
        result = service.create_event(title, date_str)
        
        # Log locally
        Schedule.objects.create(
            title=title,
            due_date=date_str, # In real app, parse to datetime
            user=user,
            google_event_id=result.get('id')
        )
        return f"Scheduled '{title}' for {date_str} and synced to Google Calendar."
    except Exception as e:
        return f"Error scheduling event: {str(e)}"

def get_market_brief(user_id=None):
    """
    Fetches a summary of the current USD/ETB rate and top market news.
    """
    market = MarketDataService()
    rate = market.get_usd_etb_rate()
    news = market.get_market_news()
    
    news_formatted = "\n".join([f"- {n}" for n in news])
    return f"**Market Brief**\nUSD/ETB Rate: {rate} Br\n\nTop News:\n{news_formatted}"

TOOLS_SCHEMA = [log_transaction, schedule_compliance_event, get_market_brief]

def handle_function_call(function_name, args):
    if function_name == 'log_transaction':
        return log_transaction(**args)
    elif function_name == 'schedule_compliance_event':
        return schedule_compliance_event(**args)
    elif function_name == 'get_market_brief':
        return get_market_brief(**args)
    return "Function not found."

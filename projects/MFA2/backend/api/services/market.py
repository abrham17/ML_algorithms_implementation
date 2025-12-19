import random

class MarketDataService:
    """
    Service to fetch Forex rates and Financial News.
    """
    
    def get_usd_etb_rate(self):
        """
        Fetches the current 1 USD to ETB rate.
        """
        # Mocking a fluctuating rate around 110-120 ETB (Official) / Black market higher
        # For this system, let's assume bank rate + small random fluctuation
        base_rate = 115.00
        fluctuation = random.uniform(-0.5, 0.5)
        return round(base_rate + fluctuation, 2)

    def get_market_news(self, query="business"):
        """
        Fetches simplified market news headlines.
        """
        # Mock news data
        return [
            "Ethiopian Coffee exports rise by 15% in Q3.",
            "New import directives issued for electronics.",
            "Global tech prices stabilize after chip shortage resolution."
        ]

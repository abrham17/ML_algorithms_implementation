from django.test import TestCase
from api.services.calendar import GoogleCalendarService
from api.services.market import MarketDataService
from api.models import CustomUser, Schedule
from api.mcp.tools import schedule_compliance_event, get_market_brief

class AdvancedIntegrationsTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testowner', role='OWNER')

    def test_market_service(self):
        service = MarketDataService()
        rate = service.get_usd_etb_rate()
        self.assertIsInstance(rate, float)
        self.assertTrue(rate > 0)
        
        news = service.get_market_news()
        self.assertTrue(len(news) > 0)

    def test_calendar_service_mock(self):
        service = GoogleCalendarService(self.user)
        event = service.create_event("Test Event", "2025-01-01")
        self.assertEqual(event['status'], 'confirmed')

    def test_mcp_schedule_tool(self):
        result = schedule_compliance_event("Tax Payment", "2025-10-10", self.user.id)
        self.assertIn("Scheduled", result)
        self.assertTrue(Schedule.objects.filter(title="Tax Payment").exists())

    def test_mcp_market_tool(self):
        result = get_market_brief()
        self.assertIn("USD/ETB Rate", result)
        self.assertIn("Top News", result)

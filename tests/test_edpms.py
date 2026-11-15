import unittest
from edpms.engine import EDPMSForexSettlementEngine, ExportShippingBill, InwardFIRCReceipt

class TestEDPMSForex(unittest.TestCase):
    def test_edpms_realization_and_forex_gain(self):
        engine = EDPMSForexSettlementEngine()
        bill = ExportShippingBill(
            shipping_bill_number="SB-998811",
            customs_port_code="INNSA1", # Nhava Sheva
            shipping_bill_date="2026-01-10",
            fob_amount_usd=50000.0,
            exchange_rate_on_shipping_date=83.00 # ₹83.00 at booking
        )

        # Inward SWIFT FIRC received on March 15 at ₹84.50
        firc = InwardFIRCReceipt(
            firc_number="FIRC-HDFC-991",
            swift_reference="SWIFT-CHASUS33-001",
            remittance_date="2026-03-15",
            currency="USD",
            remitted_amount_foreign=50000.0,
            realized_bank_exchange_rate=84.50
        )

        res = engine.process_export_realization(
            bill=bill,
            firc=firc,
            allocated_usd=50000.0,
            current_date_str="2026-03-16"
        )

        self.assertEqual(res.outstanding_balance_usd, 0.0)
        self.assertEqual(res.status, "FULLY_SETTLED_EDPMS")
        self.assertFalse(res.is_caution_listed_risk)
        # Forex gain = 50,000 * (84.50 - 83.00) = 50,000 * 1.50 = 75,000 INR
        self.assertEqual(res.forex_realized_gain_loss_inr, 75000.0)

if __name__ == "__main__":
    unittest.main()

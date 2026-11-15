"""RBI EDPMS/IDPMS Shipping Bill Tracking & Ind AS 21 Forex Realization Ledger."""

from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class ExportShippingBill:
    shipping_bill_number: str
    customs_port_code: str
    shipping_bill_date: str  # YYYY-MM-DD
    fob_amount_usd: float
    exchange_rate_on_shipping_date: float
    realized_amount_usd: float = 0.0
    is_settled_on_edpms: bool = False


@dataclass
class InwardFIRCReceipt:
    firc_number: str
    swift_reference: str
    remittance_date: str
    currency: str
    remitted_amount_foreign: float
    realized_bank_exchange_rate: float
    bank_charges_inr: float = 0.0


@dataclass
class EDPMSRealizationSummary:
    shipping_bill_number: str
    fob_amount_usd: float
    realized_usd: float
    outstanding_balance_usd: float
    statutory_9month_deadline: str
    is_caution_listed_risk: bool
    forex_realized_gain_loss_inr: float
    status: str  # FULLY_SETTLED_EDPMS, PARTIALLY_SETTLED, OVERDUE_CAUTION_LIST


class EDPMSForexSettlementEngine:
    """Manages RBI EDPMS/IDPMS export realization timeframes and Ind AS 21 foreign exchange gain/loss ledgers."""

    # RBI statutory realization timeline: 9 months from date of shipment
    STATUTORY_REALIZATION_DAYS = 270

    def process_export_realization(
        self,
        bill: ExportShippingBill,
        firc: InwardFIRCReceipt,
        allocated_usd: float,
        current_date_str: str
    ) -> EDPMSRealizationSummary:
        ship_dt = datetime.strptime(bill.shipping_bill_date, "%Y-%m-%d").date()
        deadline_dt = ship_dt + timedelta(days=self.STATUTORY_REALIZATION_DAYS)
        deadline_str = deadline_dt.strftime("%Y-%m-%d")

        curr_dt = datetime.strptime(current_date_str, "%Y-%m-%d").date()
        is_overdue = curr_dt > deadline_dt

        bill.realized_amount_usd += allocated_usd
        outstanding_usd = max(0.0, round(bill.fob_amount_usd - bill.realized_amount_usd, 2))

        # Ind AS 21: Gain/Loss = Realized Amount * (Realized Rate - Booking Rate)
        rate_diff = firc.realized_bank_exchange_rate - bill.exchange_rate_on_shipping_date
        forex_gain_loss = round(allocated_usd * rate_diff, 2)

        if outstanding_usd == 0.0:
            bill.is_settled_on_edpms = True
            status = "FULLY_SETTLED_EDPMS"
        elif is_overdue:
            status = "OVERDUE_CAUTION_LIST"
        else:
            status = "PARTIALLY_SETTLED"

        return EDPMSRealizationSummary(
            shipping_bill_number=bill.shipping_bill_number,
            fob_amount_usd=bill.fob_amount_usd,
            realized_usd=round(bill.realized_amount_usd, 2),
            outstanding_balance_usd=outstanding_usd,
            statutory_9month_deadline=deadline_str,
            is_caution_listed_risk=is_overdue and outstanding_usd > 0,
            forex_realized_gain_loss_inr=forex_gain_loss,
            status=status
        )

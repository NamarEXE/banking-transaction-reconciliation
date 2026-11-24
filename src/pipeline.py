import logging
from ingest import ingest_bank_transactions,  ingest_payment_transactions
from data_quality import analyse_data_quality
from quarantine import partition_transactions, export_results
from pathlib import Path


##configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_pipeline():
    ##start pipeline
    logger.info("Banking reconciliation ingestion pipeline started")

    ##ingestion
    bank_transactions = ingest_bank_transactions("data/raw/bank_transactions.csv")
    logger.info("Bank transactions ingested: %d",len(bank_transactions))
    payment_transactions = ingest_payment_transactions("data/raw/payment_transactions.json")
    logger.info("Payment transactions ingested: %d",len(payment_transactions))

    ## analyse data quality 
    bank_quality = analyse_data_quality(bank_transactions,"bank")
    payments_quality = analyse_data_quality(payment_transactions,"payments")
    logger.info("Bank data quality: %d valid, %d invalid",bank_quality["valid_count"],bank_quality["invalid_count"])
    logger.info("Bank duplicate transaction IDs: %s",bank_quality["duplicate_ids"])
    logger.info("Payments data quality: %d valid, %d invalid",payments_quality["valid_count"], payments_quality["invalid_count"])
    logger.info("Payment duplicate transaction IDs: %s",payments_quality["duplicate_ids"])

    ##partionioning data
    partitioned_bank_data = partition_transactions(bank_transactions,"bank")
    partitioned_payments_data = partition_transactions(payment_transactions,"payments")

    ## bank records partition log
    logger.info("Bank records accepted: %d",len(partitioned_bank_data["accepted_records"]))
    if(len(partitioned_bank_data["quarantined_records"])>0):
        logger.warning("Bank records quarantined: %d",len(partitioned_bank_data["quarantined_records"]))
    ## payments records partition log
    logger.info("Payment records accepted: %d",len(partitioned_payments_data["accepted_records"]))
    if(len(partitioned_payments_data["quarantined_records"])>0):
        logger.warning("Payments records quarantined: %d",len(partitioned_payments_data["quarantined_records"]))


    ##export results:
    ##checks output directory exists and if not creates it
    Path("data/processed").mkdir(
    parents=True,
    exist_ok=True
    )


    export_results(partitioned_bank_data,"data/processed/bank_accepted.json","data/processed/bank_quarantine.json")
    export_results(partitioned_payments_data,"data/processed/payment_accepted.json","data/processed/payment_quarantine.json")

    logger.info("results exported successfully")
    logger.info("Pipeline ran successfully")

if __name__ == "__main__":
    
    try:
        run_pipeline()
    except Exception:
        logger.exception("Banking ingestion pipeline failed")
        raise



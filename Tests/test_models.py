from Models.models import db, Receipt

def test_count_receipts(init_database, logger):
    """Test creation in the database."""
    r1 = Receipt(date="2022-01-01", category="Food", total=15.0)
    r2 = Receipt(date="2022-01-02", category="Gas", total=30.0)
    db.session.add(r1)
    db.session.add(r2)
    db.session.commit()

    # retrieved_r1 = db.session.get(Receipt, r1.id)
    receipt_count = db.session.query(Receipt).count()

    logger.info(f"Number of receipts in the database: {receipt_count}")
    assert receipt_count == 2

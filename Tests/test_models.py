from Models.models import db, Receipt

def test_count_receipts(init_database, logger):
    """Test creation in the database."""
    r1 = Receipt(date="2022-01-01", category="Food", total_amount=15.0, status="unverified", date_created="2022-01-01")
    db.session.add(r1)
    db.session.commit()
    # print(db.session.get(Receipt,r1.id),":::")
    assert db.session.get(Receipt,r1.id) is not None

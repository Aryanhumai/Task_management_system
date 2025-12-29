from sqlalchemy.orm import Session
from sqlalchemy import func


def generate_custom_id(db: Session, model, id_column: str, prefix: str) -> str:
    max_id = (
        db.query(func.max(getattr(model, id_column)))
        .filter(getattr(model, id_column).like(f"{prefix}%"))
        .scalar()
    )

    if max_id:
        last_number = int(max_id.replace(prefix, ""))
    else:
        last_number = 0

    new_number = last_number + 1
    return f"{prefix}{new_number:03d}"  # Example: P001, T015
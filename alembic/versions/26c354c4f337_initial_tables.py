"""Initial Tables

Revision ID: 26c354c4f337
Revises: 
Create Date: 2023-04-14 15:43:38.602456

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "26c354c4f337"
down_revision = None
branch_labels = None
depends_on = None


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_values_count", table_name="values")
    op.drop_index("ix_values_id", table_name="values")
    op.drop_index("ix_values_timestamp", table_name="values")
    op.drop_index("ix_values_value", table_name="values")
    op.drop_table("values")
    op.drop_index("ix_sensors_device_class", table_name="sensors")
    op.drop_index("ix_sensors_name", table_name="sensors")
    op.drop_index("ix_sensors_state_topic", table_name="sensors")
    op.drop_index("ix_sensors_uniq_id", table_name="sensors")
    op.drop_index("ix_sensors_unit_of_measurement", table_name="sensors")
    op.drop_table("sensors")
    # ### end Alembic commands ###


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "sensors",
        sa.Column("name", sa.VARCHAR(), nullable=True),
        sa.Column("uniq_id", sa.VARCHAR(), nullable=False),
        sa.Column("state_topic", sa.VARCHAR(), nullable=True),
        sa.Column("unit_of_measurement", sa.VARCHAR(), nullable=True),
        sa.Column("device_class", sa.VARCHAR(), nullable=True),
        sa.PrimaryKeyConstraint("uniq_id"),
    )
    op.create_index(
        "ix_sensors_unit_of_measurement",
        "sensors",
        ["unit_of_measurement"],
        unique=False,
    )
    op.create_index("ix_sensors_uniq_id", "sensors", ["uniq_id"], unique=False)
    op.create_index("ix_sensors_state_topic", "sensors", ["state_topic"], unique=False)
    op.create_index("ix_sensors_name", "sensors", ["name"], unique=False)
    op.create_index(
        "ix_sensors_device_class", "sensors", ["device_class"], unique=False
    )
    op.create_table(
        "values",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("count", sa.INTEGER(), nullable=True),
        sa.Column("value", sa.VARCHAR(), nullable=True),
        sa.Column("timestamp", sa.DATETIME(), nullable=True),
        sa.Column("sensor_id", sa.VARCHAR(), nullable=True),
        sa.ForeignKeyConstraint(
            ["sensor_id"],
            ["sensors.uniq_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_values_value", "values", ["value"], unique=False)
    op.create_index("ix_values_timestamp", "values", ["timestamp"], unique=False)
    op.create_index("ix_values_id", "values", ["id"], unique=False)
    op.create_index("ix_values_count", "values", ["count"], unique=False)
    # ### end Alembic commands ###

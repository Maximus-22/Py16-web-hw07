"""'Init'

Revision ID: 4ed5c84f6ee7
Revises: 
Create Date: 2023-11-04 20:16:16.157314

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ed5c84f6ee7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users-faker')
    op.alter_column('grades', 'grade',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('grades', 'grade_date',
               existing_type=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('grades', 'grade_date',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('grades', 'grade',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_table('users-faker',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=60), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=60), autoincrement=False, nullable=True),
    sa.Column('password', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
    sa.Column('age', sa.SMALLINT(), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(length=24), autoincrement=False, nullable=True),
    sa.CheckConstraint('age >= 18 AND age <= 75', name='students_age_check'),
    sa.PrimaryKeyConstraint('id', name='students_pkey')
    )
    # ### end Alembic commands ###

"""empty message

Revision ID: 4171b1a82bdc
Revises: 0f06edb6ca39
Create Date: 2020-09-14 22:39:38.106299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4171b1a82bdc'
down_revision = '0f06edb6ca39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('seeking_description',
                                       sa.String(length=300), nullable=True))
    op.add_column('artists', sa.Column(
        'seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('artists', sa.Column(
        'website', sa.String(length=120), nullable=True))
    op.execute(
        'UPDATE artists SET seeking_venue = False WHERE seeking_venue IS Null;')
    op.alter_column('artists', 'seeking_venue',
                    existing_type=sa.Boolean(),
                    nullable=False)

    op.add_column('venues', sa.Column('genres', sa.ARRAY(
        sa.String(), dimensions=1), nullable=True))
    op.add_column('venues', sa.Column('seeking_description',
                                      sa.String(length=300), nullable=True))
    op.add_column('venues', sa.Column(
        'seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('venues', sa.Column(
        'website', sa.String(length=120), nullable=True))
    op.execute(
        'UPDATE venues SET seeking_talent = False WHERE seeking_talent IS Null;')
    op.alter_column('venues', 'seeking_talent',
                    existing_type=sa.Boolean(),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venues', 'name',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.drop_column('venues', 'website')
    op.drop_column('venues', 'seeking_talent')
    op.drop_column('venues', 'seeking_description')
    op.drop_column('venues', 'genres')
    op.alter_column('artists', 'name',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.drop_column('artists', 'website')
    op.drop_column('artists', 'seeking_venue')
    op.drop_column('artists', 'seeking_description')
    # ### end Alembic commands ###
"""empty message

Revision ID: 3f61f92ee74a
Revises: bd44c2f05785
Create Date: 2024-04-16 21:35:32.252053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f61f92ee74a'
down_revision = 'bd44c2f05785'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('jurisdiction', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('upvotes', sa.Integer(), nullable=True))
        batch_op.create_unique_constraint("unique_title_constraint", ['title'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('upvotes')
        batch_op.drop_column('jurisdiction')

    op.create_table('comment',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('text', sa.VARCHAR(length=600), nullable=True),
    sa.Column('post_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
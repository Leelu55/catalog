from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Base, Book, User

engine = create_engine('postgresql://catalog:password@localhost:5432/catalog')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


# Create all Categories, these are only editable and extendable by the admin
category1 = Category(name="Children's Books",
                     image="cat_child.jpg"
                     )
category2 = Category(name="Fiction",
                     image="cat_fiction.jpg"
                     )
category3 = Category(name="Non-Fiction",
                     image="cat_nonfict.jpg"
                     )
category4 = Category(name="Graphic Novel",
                     image="cat_graphnov.png"
                     )
category5 = Category(name="Poetry",
                     image="cat_poetry.jpg"
                     )
user1 = User(name="Admin User", email="maria@yalpani.de")

session.add(category1)
session.add(category2)
session.add(category3)
session.add(category4)
session.add(category5)
session.commit()

# Initial Books in Children's Books (category1)
book1 = Book(title="Alice in Wonderland",
             author="Lewis Caroll",
             description="While chasing a white rabbit Alice gets lost in a\
                     crazy magic world.",
             category_id=category1.id,
             user_id=1,
             image="ch_aiw_lc.jpg"
             )

book2 = Book(title="Anne of Green Gables",
             author="Lucy Maud Montgomery",
             description="Anne, an orphan with lots of fantasy and affection\
                     gets adopted by elderly siblings in Avonlea and becomes \
                     happy while growing up in this Coming-of-Age novel.",
             category_id=category1.id,
             user_id=1,
             image="ch_aog_lmm.jpg"
             )

book3 = Book(title="Winnie-the-Pooh",
             author="A.A.Milne",
             description="Christopher Robin follows his Teddy Bear \
                     Winnie-the-Pooh into his world in the woods and goes on \
                     adventures with him and his friends.",
             category_id=category1.id,
             user_id=1,
             image="ch_wp_aam.jpg"
             )

session.add(book1)
session.add(book2)
session.add(book3)
session.commit()

# Initial Books in Fiction (category2)
book4 = Book(title="Outside Looking In",
             author="T.C. Boyle",
             description="A group of scientists and students explore the \
                     psychodelic and mind changing effects of LSD and the \
                     consequences of it's use on their lifes.",
             category_id=category2.id,
             user_id=1,
             image="f_oli_tcb.jpg"
             )

book5 = Book(title="The Visitors",
             author="Sally Beauman",
             description="In this Coming-of-Age novel set in Egypt and England\
                    we experience the discovery of Tutankhamun's grave in 1922\
                    and it's effects on all the people who were there.\
                    Fictionalized but with some historic accuracy it is a \
                    thrilling and touching account told by Lucy,\
                    growing up in turbulent time and company.",
             category_id=category2.id,
             user_id=1,
             image="f_tv_sb.jpg"
             )

book6 = Book(title="The Moon is a Harsh Mistress",
             author="Robert A. Heinlein",
             description="A lunar colony revolts against the rulers on earth \
                     in search of liberty",
             category_id=category2.id,
             user_id=1,
             image="f_tmiahm_rah.jpg"
             )

session.add(book4)
session.add(book5)
session.add(book6)
session.commit()

# Initial Books in Non-Fiction (category3)

book7 = Book(title="The Secret Poisoner",
             author="Linda Stratmann",
             description="Explores the history of poisoning in \
                     Victorian times",
             category_id=category3.id,
             user_id=1,
             image="nf_tsp_ls.jpg"
             )

book8 = Book(title="The Book of Palms",
             author="Carl Friedrich Philipp von Martius",
             description="Reprint of an illustrated comprehensive 19. century \
                     work on palms",
             category_id=category3.id,
             user_id=1,
             image="nf_tbop_cfpm.jpg"
             )

session.add(book7)
session.add(book8)
session.commit()

# Initial Books in Graphic Novels (category4)


book9 = Book(title="Aya",
             author="Marguerite Abouet",
             description="Coming of Age in Abidjan in the 70ies is not always \
                     easy but very exiting for Aya and her friends.",
             category_id=category4.id,
             user_id=1,
             image="gn_aya_ma.jpg"
             )

book10 = Book(title="Pyongyang: A Journey in North Korea",
              author="Guy Delisle",
              description="An autobiographical, insightful and very funny \
                     graphic account of the author's professional stay as\
                     an animator in communist North Korea",
              category_id=category4.id,
              user_id=1,
              image="gn_pj_gd.jpg"
              )

session.add(book9)
session.add(book10)
session.commit()

# Initial Books in Poetry (category5)

book11 = Book(title="Late Poems",
              author="Anna Akhmatova",
              description="A collection of the late poems of the most famous \
                     russian poet Anna Akhmatova",
              category_id=category5.id,
              user_id=1,
              image="p_poetry_aa.jpg"
              )

book12 = Book(title="Poems",
              author="Georg Trakl",
              description="Expressionist poems about Death, Delusion and \
                     Desperation",
              category_id=category5.id,
              user_id=1,
              image="p_poems_gt.jpg"
              )

session.add(book11)
session.add(book12)
session.commit()


print "added initial data!"

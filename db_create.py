from catalog import db
from catalog.models import Base, Category, Item, User



def main():
    #drop the database tables
    #create the database and the tables
    db.drop_all()
    db.create_all()
        # Create stock, out of the box user
    UserArtV = User(name="Art Vandalay",
                    email="art.vandalay@vandalayindustries.com",
                    picture="/static/costanza.jpg")
    db.session.add(UserArtV)
    db.session.commit()

    category1 = Category(name="Soccer")
    db.session.add(category1)
    db.session.commit()

    category2 = Category(name="Basketball")
    db.session.add(category2)
    db.session.commit()

    category3 = Category(name="Baseball")
    db.session.add(category3)
    db.session.commit()

    category4 = Category(name="Frisbee")
    db.session.add(category4)
    db.session.commit()

    category5 = Category(name="Snowboarding")
    db.session.add(category5)
    db.session.commit()

    category6 = Category(name="Rock Climbing")
    db.session.add(category6)
    db.session.commit()

    category7 = Category(name="Foosball")
    db.session.add(category7)
    db.session.commit()

    category8 = Category(name="Skating")
    db.session.add(category8)
    db.session.commit()

    category9 = Category(name="Hockey")
    db.session.add(category9)
    db.session.commit()

    item1 = Item(user_id=1, name="Stick", description="Interdum odio dignissim in nisi metus\
                 , a elit sit dis cubilia, fringilla praesent pulvinar porta.\
                 Sodales hac bibendum", category=category9)
    db.session.add(item1)
    db.session.commit()

    item2 = Item(user_id=1, name="Goggles",
                 description="Primis dignissim mattis erat bibendum eu arcu quis\
                  cursus", category=category5)
    db.session.add(item2)
    db.session.commit()

    item3 = Item(user_id=1, name="Snowboard",
                 description="Curae feugiat netus auctor lacus",
                 category=category5)
    db.session.add(item3)
    db.session.commit()

    item4 = Item(user_id=1, name="Soccer Item 1", description="Nec odio consectetur cum \
                 consequat quam massa habitant placerat, nam tincidunt mi egestas \
                 eu taciti velit dictum aenean, vestibulum inceptos semper \
                 penatibus proin fringilla quisque. Cursus ridiculus facilisis \
                 class erat varius cum consequat, ac at justo mattis magna dui \
                 suscipit interdum, faucibus auctor rhoncus diam parturient a.",
                 category=category1)
    db.session.add(item4)
    db.session.commit()

    item5 = Item(user_id=1, name="Soccer Item 2", description="Fermentum scelerisque \
                 facilisis tortor rhoncus magna maecenas, blandit ligula metus \
                 amet congue fames pulvinar, eget aliquam augue eros per. Vel \
                 etiam dolor ornare aliquet posuere inceptos maecenas nam, varius \
                 eget ad imperdiet mi phasellus turpis nisl libero, urna \
                 tristique aptent ultricies taciti montes parturient.",
                 category=category1)
    db.session.add(item5)
    db.session.commit()

    item6 = Item(user_id=1, name="Soccer Item 3", description="Placerat primis taciti etiam \
                 ut convallis accumsan lorem tortor sapien faucibus cursus, quam \
                 nulla tempor morbi rhoncus suscipit sociis in litora amet enim, \
                 praesent aptent bibendum integer ornare dapibus justo rutrum \
                 aliquet vivamus. Taciti dignissim neque euismod elit maecenas \
                 aptent interdum mollis vel sociosqu donec, nunc gravida eget ad \
                 quisque viverra vitae amet hendrerit.", category=category1)
    db.session.add(item6)
    db.session.commit()

    item7 = Item(user_id=1, name="Soccer Item 4", description="Litora turpis et dignissim \
                 nascetur faucibus taciti vivamus interdum, tempor dapibus lorem \
                 venenatis enim conubia lacus netus hac, dis magnis vel nulla \
                 phasellus bibendum fringilla. Sed torquent taciti accumsan elit \
                 sagittis nulla magnis, sit praesent volutpat nam consectetur \
                 velit, magna sociis id ultrices diam non.", category=category1)
    db.session.add(item7)
    db.session.commit()

    item8 = Item(user_id=1, name="Frisbee", description="Interdum odio dignissim in nisi \
                 metus, a elit sit dis cubilia, fringilla praesent pulvinar \
                 porta. Sodales hac bibendum tincidunt risus mus himenaeos erat \
                 ac, mollis semper integer tempor lacus turpis libero, ridiculus \
                 primis curae aliquet nec rhoncus ante.", category=category4)
    db.session.add(item8)
    db.session.commit()

    item9 = Item(user_id=1, name="Bat",
                 description="Primis dignissim mattis erat bibendum eu arcu \
        quis cursus", category=category3)
    db.session.add(item9)
    db.session.commit()

    #commit changes
    db.session.commit()

    print "Added Categories, Items, and a User."

if __name__ == '__main__':
    main()

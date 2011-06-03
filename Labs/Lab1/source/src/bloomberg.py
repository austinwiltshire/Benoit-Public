

import sqlalchemy
import sqlalchemy.orm

ENGINE = sqlalchemy.create_engine("mysql://" \
                                  "austinwiltshire" \
                                  "@richie" \
                                  ":3306" \
                                  "/bloomberg_v2",
                                  echo = False)

D_ENGINE = sqlalchemy.create_engine("mysql://" \
                                  "austinwiltshire" \
                                  "@richie" \
                                  ":3306" \
                                  "/bloomberg_v2",
                                  echo = True) 

SESSION = sqlalchemy.orm.sessionmaker(ENGINE)()
D_SESSION = sqlalchemy.orm.sessionmaker(D_ENGINE)()
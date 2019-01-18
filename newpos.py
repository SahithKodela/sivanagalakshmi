from flask import Flask,request,abort
from flask_restful import Resource, Api
from newarrivals import productDetail,AddToCartSite,Catsubcat,Allategories,Categories,ResetPassword,ForgotPassword,LogOut,HomePage,Service,OffersCat,NewArrivalCat,MobileHomePage,MobileOffersCat,MobileNewArrivalCat,OffersCatAll,NewArrivalCatAll,Test,Test123,MobileNewArrivalCatAll,MobileOffersCatAll
import datetime
from time import strftime

newapp = Flask(__name__)
api = Service(newapp)

api.add_resource(HomePage, '/homepage')
api.add_resource(OffersCat, '/offerscats')
api.add_resource(NewArrivalCat, '/newarrivtest123alcats')
api.add_resource(OffersCatAll, '/offerscatsall')
api.add_resource(NewArrivalCatAll, '/newarrivalcatsall')
api.add_resource(Test, '/test')
api.add_resource(Test123, '/test123')
api.add_resource(LogOut,'/logout')
api.add_resource(ForgotPassword,'/forgot')
api.add_resource(ResetPassword,'/reset')
api.add_resource(Categories,'/categories')
api.add_resource(Allategories,'/allcategories')
api.add_resource(Catsubcat,'/catsubcat')
api.add_resource(productDetail,'/productdtl')
api.add_resource(AddToCartSite,'/addtocart')
#api.add_resource(GetCart,'/getcart')



#-------------------------------Mobile------------------------
api.add_resource(MobileHomePage, '/mobile_homepage')
api.add_resource(MobileOffersCat, '/mobile_offerscats')
api.add_resource(MobileNewArrivalCat, '/mobile_newarrivalcats')
api.add_resource(MobileOffersCatAll, '/mobile_offerscatsall')
api.add_resource(MobileNewArrivalCatAll, '/mobile_newarrivalcatsall')


#--------------------------------------------Loggers---------------------------------------------------
import logging

log = logging.getLogger("__name__")
@newapp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,secret_key')

    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        log.error('%s %s %s %s %s %s',
                  ts,
                  request.remote_addr,
                  request.method,
                  request.scheme,
                  request.full_path,
                  response.status)
    return response

#-----------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    newapp.run(host='192.168.20.65',port=5000)


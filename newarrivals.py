from flask_restful import Resource,Api
from flask import jsonify, request
from models import *
import json
import datetime
from time import strftime
from itertools import groupby
import operator
import itertools
import onetimepass as otp
from threading import Thread

secret_key = '1234'

#------------------------------Loggers------------------------------------------------------
import logging
from logging.handlers import RotatingFileHandler
from flask_restful import Resource, Api
import traceback
from time import strftime

log = logging.getLogger("__name__")
class Service(Api):
    def handle_error(self, e):
        if not hasattr(e, 'data'):
            e.data = e
            ts = strftime('[%Y-%b-%d %H:%M:%S]')
            tb = traceback.format_exc()
            log.error('%s %s %s %s %s 500 INTERNAL SERVER ERROR\n%s',
                          ts, 
                          request.remote_addr, 
                          request.method,
                          request.scheme, 
                          request.full_path, 
                          tb)
        return super(Service, self).handle_error(traceback.format_exc(e))

#---------------------------------------------------------------------------------------------

class HomePage(Resource):
    def get(self):
       if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
         log.info('Entered into home services')  
         coll=Collections.objects.order_by('-id')
         collections = json.loads(coll.to_json())
         tbrd=Brand.objects(brandtype='Top Brands').order_by('-id')
         topbrands = json.loads(tbrd.to_json())
         ebrd=Brand.objects(brandtype='Emerging Brands').order_by('-id')
         emergingbrands = json.loads(ebrd.to_json())
         baners=Banner.objects.order_by('-id')
         baner = json.loads(baners.to_json())
         deals=[]
         for productname in Sup_Upload.objects():
          product=productname.upload_name
          if ',' in product and not product.endswith(','):
            related_prod=Sup_Upload.objects(upload_name=product,upload_category="Deals",status="Accept").filter(prices__doubleoffer_price__gt=0.0).only('avgrating','upload_name','upload_photo','upload_category','upload_subcategory','prices.offer_price','prices.enduser_price','prices.percentage','attributes.atrname','attributes.atrvalue')[0:10]
            for prods in related_prod:
                deal=json.loads(prods.to_json())
                deals.append(deal)
         log.info('Display the home services')
         #args = request.args['upload_subcategory']
         data=[]
         invalid_list=Sup_Upload.objects(upload_category__ne="Deals",status='Accept').filter(prices__doubleoffer_price__gt=0.0).order_by('-prices.percentage')[0:10]
         for invalid_info in invalid_list:
            details={}
            details['avgrating']=invalid_info.avgrating
            details['upload_name']=invalid_info.upload_name
            details['upload_brand']=invalid_info.upload_brand
            details['upload_subcategory']=invalid_info.upload_subcategory
            details['upload_category']=invalid_info.upload_category
            details['upload_photo']=invalid_info.upload_photo
            attr_data=[]
            for attr in invalid_info.attributes:
                attr_details={}
                attr_details['atrname']=attr.atrname
                attr_details['atrvalue']=attr.atrvalue
                attr_data.append(attr_details)
            details['attributes']=attr_data
            for price in invalid_info.prices:
                details['doubleoffer_price']=price.doubleoffer_price
                details['offer_price']=price.offer_price
                details['enduser_price']=price.enduser_price
                details['percentage']=price.percentage
                data.append(details)
               
            dealslist = invalid_info.todaydeals
            if len(dealslist)>0:
                if dealslist[0].status=='True':
                        details['special_offer']=dealslist[0].special_discount
                        details['special_percentage']=dealslist[0].percentage
                        data.append(details)
            else:
                details['special_offer']='0'
                data.append(details)
        
              
         getvals = operator.itemgetter('upload_name')
         data.sort(key=getvals)
         result = []        
         for k, g in itertools.groupby(data, getvals):
            result.append(g.next())
         #print result
         #keyfunc = lambda d: (d['upload_name'])
         #giter = groupby(sorted(data, key=keyfunc), keyfunc)
         #product = [g[1].next() for g in giter]        
         #args = request.args['upload_subcategory']
         log.info('Display the newarrivals')
         data=[]
         invalid_list=Sup_Upload.objects(upload_category__ne="Deals",status='Accept').filter(prices__doubleoffer_price__gt=0.0).order_by('-id')[0:10]
         for invalid_info in invalid_list:
            details={}
            details['avgrating']=invalid_info.avgrating
            details['upload_name']=invalid_info.upload_name
            details['upload_brand']=invalid_info.upload_brand
            details['upload_subcategory']=invalid_info.upload_subcategory
            details['upload_category']=invalid_info.upload_category
            details['upload_photo']=invalid_info.upload_photo
            attr_data=[]
            for attr in invalid_info.attributes:
                attr_details={}
                attr_details['atrname']=attr.atrname
                attr_details['atrvalue']=attr.atrvalue
                attr_data.append(attr_details)
            details['attributes']=attr_data
            for price in invalid_info.prices:
                details['doubleoffer_price']=price.doubleoffer_price
                details['offer_price']=price.offer_price
                details['enduser_price']=price.enduser_price
                details['percentage']=price.percentage
                
                
            dealslist = invalid_info.todaydeals
            if len(dealslist)>0:
                if dealslist[0].status=='True':
                        details['special_offer']=dealslist[0].special_discount
                        details['special_percentage']=dealslist[0].percentage
                        data.append(details)
            else:
                details['special_offer']='0'
                data.append(details)
                
         keyfunc = lambda d: (d['upload_name'])
         giter = groupby(sorted(data, key=keyfunc), keyfunc)
         product = [g[1].next() for g in giter]
         coupons=[]         
         for coupon in OrderCoupons.objects(status="Active"):
            edate=datetime.datetime.strptime(coupon.end_date, '%d/%m/%Y')
            enddate= edate.date()
            fdate=datetime.datetime.strptime(coupon.from_date, '%d/%m/%Y')
            fromdate= fdate.date()
            if fromdate<=enddate:
                 discount=str(coupon.discount)+str(coupon.typef)
                 details={}
                 details['coupon_name']=coupon.coupon_name
                 details['coupon_code']=coupon.coupon_code
                 details['imageurl']=coupon.imageurl
                 details['discount']=discount
                 details['end_date']=coupon.end_date
                 #json_info=json.loads(json.dumps(details))
                 coupons.append(details)
         return {'baner':baner,'status':'Success','topbrands':topbrands,'collections':collections,'emergingbrands':emergingbrands,"deals":deals,'coupons':coupons,"offerscats":result,"newarrivalcats":product}


class OffersCat(Resource):
    def get(self):
       if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
         args = request.args['upload_subcategory']
         #print args,"ram"
         data=[]
         invalid_list=Sup_Upload.objects(upload_category__ne="Deals",upload_subcategory__icontains=args,status='Accept').filter(prices__doubleoffer_price__gt=0.0).order_by('-prices.percentage')[0:10]
         #(Q(snapshot_values__key__in=key_list) & Q(snapshot_values__value__in=value_list).order_by('-todaydeals.percentage')
         '''
         for dealslist in invalid_list.todaydeals:
             if len(dealslist)>0:
                 print "if"
                 dealslist.order_by('-todaydeals.percentage')
             else:
                 print "else"
                 dealslist.order_by('-prices.percentage')
         '''        
         for invalid_info in invalid_list:
                details={}
                details['avgrating']=invalid_info.avgrating
                details['upload_name']=invalid_info.upload_name
                details['upload_brand']=invalid_info.upload_brand
                details['upload_subcategory']=invalid_info.upload_subcategory
                details['upload_category']=invalid_info.upload_category
                details['upload_photo']=invalid_info.upload_photo
                #details['extraimages']=invalid_info.extraimages
                
                attr_data=[]
                for attr in invalid_info.attributes:
                    attr_details={}
                    attr_details['atrname']=attr.atrname
                    attr_details['atrvalue']=attr.atrvalue
                    attr_data.append(attr_details)
                details['attributes']=attr_data
                for price in invalid_info.prices:
                    details['doubleoffer_price']=price.doubleoffer_price
                    details['offer_price']=price.offer_price
                    details['enduser_price']=price.enduser_price
                    details['percentage']=price.percentage
                dealslist = invalid_info.todaydeals
                if len(dealslist)>0:
                    if dealslist[0].status=='True':
                            details['special_offer']=dealslist[0].special_discount
                            details['special_percentage']=dealslist[0].percentage
                            data.append(details)
                else:
                    details['special_offer']='0'
                    data.append(details)
                        
                    
         keyfunc = lambda d: (d['upload_name'])
         giter = groupby(sorted(data, key=keyfunc), keyfunc)
         product = [g[1].next() for g in giter]          
         
         log.info('Display the offers')
         return {'status':'Success','offerscats':product}
         
class NewArrivalCat(Resource):
    def get(self):
       if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
         args = request.args['upload_subcategory']
         #print args,"sai"
         data=[]
         invalid_list=Sup_Upload.objects(upload_category__ne="Deals",upload_subcategory__icontains=args,status='Accept').filter(prices__doubleoffer_price__gt=0.0).order_by('-id')[0:10]
         for invalid_info in invalid_list:
                details={}
                details['avgrating']=invalid_info.avgrating
                details['upload_name']=invalid_info.upload_name
                details['upload_brand']=invalid_info.upload_brand
                details['upload_subcategory']=invalid_info.upload_subcategory
                details['upload_category']=invalid_info.upload_category
                details['upload_photo']=invalid_info.upload_photo
                attr_data=[]
                for attr in invalid_info.attributes:
                    attr_details={}
                    attr_details['atrname']=attr.atrname
                    attr_details['atrvalue']=attr.atrvalue
                    attr_data.append(attr_details)
                details['attributes']=attr_data
                for price in invalid_info.prices:
                    details['doubleoffer_price']=price.doubleoffer_price
                    details['offer_price']=price.offer_price
                    details['enduser_price']=price.enduser_price
                    details['percentage']=price.percentage
                    
                dealslist = invalid_info.todaydeals
                if len(dealslist)>0:
                    if dealslist[0].status=='True':
                            details['special_offer']=dealslist[0].special_discount
                            details['special_percentage']=dealslist[0].percentage
                            data.append(details)
                else:
                    details['special_offer']='0'
                    data.append(details)
         keyfunc = lambda d: (d['upload_name'])
         giter = groupby(sorted(data, key=keyfunc), keyfunc)
         product = [g[1].next() for g in giter]                   
         return {'status':'Success','newarrivalcats':product}

class OffersCatAll(Resource):
    def get(self):
       if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
         args = request.args['upload_subcategory']
         #print args,"ar"
         if args=='All':
             data=[]
             invalid_list=Sup_Upload.objects(status='Accept').filter(prices__doubleoffer_price__gt=0.0).order_by('-prices.percentage')
             #print invalid_list,"list"
             #(Q(snapshot_values__key__in=key_list) & Q(snapshot_values__value__in=value_list).order_by('-todaydeals.percentage')
             '''
             for dealslist in invalid_list.todaydeals:
                 if len(dealslist)>0:
                     print "if"
                     dealslist.order_by('-todaydeals.percentage')
                 else:
                     print "else"
                     dealslist.order_by('-prices.percentage')
             '''        
             for invalid_info in invalid_list:
                    details={}
                    details['avgrating']=invalid_info.avgrating
                    details['upload_name']=invalid_info.upload_name
                    details['upload_brand']=invalid_info.upload_brand
                    details['upload_subcategory']=invalid_info.upload_subcategory
                    details['upload_category']=invalid_info.upload_category
                    details['upload_photo']=invalid_info.upload_photo
                    #details['extraimages']=invalid_info.extraimages
                    
                    attr_data=[]
                    for attr in invalid_info.attributes:
                        attr_details={}
                        attr_details['atrname']=attr.atrname
                        attr_details['atrvalue']=attr.atrvalue
                        attr_data.append(attr_details)
                    details['attributes']=attr_data
                    for price in invalid_info.prices:
                        details['doubleoffer_price']=price.doubleoffer_price
                        details['offer_price']=price.offer_price
                        details['enduser_price']=price.enduser_price
                        details['percentage']=price.percentage
                    dealslist = invalid_info.todaydeals
                    if len(dealslist)>0:
                        if dealslist[0].status=='True':
                                details['special_offer']=dealslist[0].special_discount
                                details['special_percentage']=dealslist[0].percentage
                                data.append(details)
                    else:
                        details['special_offer']='0'
                        data.append(details)
                            
                        
             keyfunc = lambda d: (d['upload_name'])
             giter = groupby(sorted(data, key=keyfunc), keyfunc)
             product = [g[1].next() for g in giter]          
             
             log.info('Display the offers')
             return {'status':'Success','offerscats':product}
         else:
             data=[]
             invalid_list=Sup_Upload.objects(upload_subcategory__icontains=args,status='Accept').filter(prices__doubleoffer_price__gt=0.0).order_by('-prices.percentage')
             #print invalid_list,"list"
             #(Q(snapshot_values__key__in=key_list) & Q(snapshot_values__value__in=value_list).order_by('-todaydeals.percentage')      
             for invalid_info in invalid_list:
                    details={}
                    details['avgrating']=invalid_info.avgrating
                    details['upload_name']=invalid_info.upload_name
                    details['upload_brand']=invalid_info.upload_brand
                    details['upload_subcategory']=invalid_info.upload_subcategory
                    details['upload_category']=invalid_info.upload_category
                    details['upload_photo']=invalid_info.upload_photo
                    #details['extraimages']=invalid_info.extraimages
                    
                    attr_data=[]
                    for attr in invalid_info.attributes:
                        attr_details={}
                        attr_details['atrname']=attr.atrname
                        attr_details['atrvalue']=attr.atrvalue
                        attr_data.append(attr_details)
                    details['attributes']=attr_data
                    for price in invalid_info.prices:
                        details['doubleoffer_price']=price.doubleoffer_price
                        details['offer_price']=price.offer_price
                        details['enduser_price']=price.enduser_price
                        details['percentage']=price.percentage
                    dealslist = invalid_info.todaydeals
                    if len(dealslist)>0:
                        if dealslist[0].status=='True':
                                details['special_offer']=dealslist[0].special_discount
                                details['special_percentage']=dealslist[0].percentage
                                data.append(details)
                    else:
                        details['special_offer']='0'
                        data.append(details)
                            
                        
             keyfunc = lambda d: (d['upload_name'])
             giter = groupby(sorted(data, key=keyfunc), keyfunc)
             product = [g[1].next() for g in giter]          
             
             log.info('Display the offers')
             return {'status':'Success','offerscats':product}
         
class NewArrivalCatAll(Resource):
    def get(self):
       if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
         args = request.args['upload_subcategory']
         #print args,"args"
         if args=='All':
             data=[]
             invalid_list=Sup_Upload.objects(status='Accept').filter(prices__doubleoffer_price__gt=0.0).order_by('-id')
             for invalid_info in invalid_list:
                    details={}
                    details['avgrating']=invalid_info.avgrating
                    details['upload_name']=invalid_info.upload_name
                    details['upload_brand']=invalid_info.upload_brand
                    details['upload_subcategory']=invalid_info.upload_subcategory
                    details['upload_category']=invalid_info.upload_category
                    details['upload_photo']=invalid_info.upload_photo
                    attr_data=[]
                    for attr in invalid_info.attributes:
                        attr_details={}
                        attr_details['atrname']=attr.atrname
                        attr_details['atrvalue']=attr.atrvalue
                        attr_data.append(attr_details)
                    details['attributes']=attr_data
                    for price in invalid_info.prices:
                        details['doubleoffer_price']=price.doubleoffer_price
                        details['offer_price']=price.offer_price
                        details['enduser_price']=price.enduser_price
                        details['percentage']=price.percentage
                        
                    dealslist = invalid_info.todaydeals
                    if len(dealslist)>0:
                        if dealslist[0].status=='True':
                                details['special_offer']=dealslist[0].special_discount
                                details['special_percentage']=dealslist[0].percentage
                                data.append(details)
                    else:
                        details['special_offer']='0'
                        data.append(details)
             keyfunc = lambda d: (d['upload_name'])
             giter = groupby(sorted(data, key=keyfunc), keyfunc)
             product = [g[1].next() for g in giter]                   
             return {'status':'Success','newarrivalcats':product}
         else:
             data=[]
             invalid_list=Sup_Upload.objects(upload_subcategory__icontains=args,status='Accept').filter(prices__doubleoffer_price__gt=0.0).order_by('-id')
             for invalid_info in invalid_list:
                    details={}
                    details['avgrating']=invalid_info.avgrating
                    details['upload_name']=invalid_info.upload_name
                    details['upload_brand']=invalid_info.upload_brand
                    details['upload_subcategory']=invalid_info.upload_subcategory
                    details['upload_category']=invalid_info.upload_category
                    details['upload_photo']=invalid_info.upload_photo
                    attr_data=[]
                    for attr in invalid_info.attributes:
                        attr_details={}
                        attr_details['atrname']=attr.atrname
                        attr_details['atrvalue']=attr.atrvalue
                        attr_data.append(attr_details)
                    details['attributes']=attr_data
                    for price in invalid_info.prices:
                        details['doubleoffer_price']=price.doubleoffer_price
                        details['offer_price']=price.offer_price
                        details['enduser_price']=price.enduser_price
                        details['percentage']=price.percentage
                        
                    dealslist = invalid_info.todaydeals
                    if len(dealslist)>0:
                        if dealslist[0].status=='True':
                                details['special_offer']=dealslist[0].special_discount
                                details['special_percentage']=dealslist[0].percentage
                                data.append(details)
                    else:
                        details['special_offer']='0'
                        data.append(details)
             keyfunc = lambda d: (d['upload_name'])
             giter = groupby(sorted(data, key=keyfunc), keyfunc)
             product = [g[1].next() for g in giter]                   
             return {'status':'Success','newarrivalcats':product}           
         
#--------------------------------------------------------- smobile services----------------------------------------------------------------------------------
class MobileHomePage(Resource):
    def get(self):
       if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
         log.info('Entered into home services')  
         coll=Collections.objects.order_by('-id')
         collections = json.loads(coll.to_json())
         tbrd=Brand.objects(brandtype='Top Brands').order_by('-id')
         topbrands = json.loads(tbrd.to_json())
         ebrd=Brand.objects(brandtype='Emerging Brands').order_by('-id')
         emergingbrands = json.loads(ebrd.to_json())
         baners=Banner.objects.order_by('-id')
         baner = json.loads(baners.to_json())
         deals=[]
         for productname in Sup_Upload.objects():
          product=productname.upload_name
          if ',' in product and not product.endswith(','):
            related_prod=Sup_Upload.objects(upload_name=product,upload_category="Deals",status="Accept").filter(prices__doubleoffer_price__gt=0.0).only('avgrating','upload_name','upload_photo','upload_category','upload_subcategory','prices.offer_price','prices.enduser_price','prices.percentage','attributes.atrname','attributes.atrvalue')[0:10]
            for prods in related_prod:
                deal=json.loads(prods.to_json())
                deals.append(deal)
         log.info('Display the home services')
         #args = request.args['upload_subcategory']
         data=[]
         invalid_list=Sup_Upload.objects(upload_category__ne="Deals",status='Accept').filter(prices__doubleoffer_price__gt=0.0).order_by('-prices.percentage')[0:10]
         for invalid_info in invalid_list:
            details={}
            details['avgrating']=invalid_info.avgrating
            details['upload_name']=invalid_info.upload_name
            details['upload_brand']=invalid_info.upload_brand
            details['upload_subcategory']=invalid_info.upload_subcategory
            details['upload_category']=invalid_info.upload_category
            details['upload_photo']=invalid_info.upload_photo
            details['extraimages']=invalid_info.extraimages
            attr_data=[]
            for attr in invalid_info.attributes:
                attr_details={}
                attr_details['atrname']=attr.atrname
                attr_details['atrvalue']=attr.atrvalue
                attr_data.append(attr_details)
            details['attributes']=attr_data
            for price in invalid_info.prices:
                details['doubleoffer_price']=price.doubleoffer_price
                details['offer_price']=price.offer_price
                details['enduser_price']=price.enduser_price
                details['percentage']=price.percentage
                data.append(details)
               
            dealslist = invalid_info.todaydeals
            if len(dealslist)>0:
                if dealslist[0].status=='True':
                        details['special_offer']=dealslist[0].special_discount
                        details['special_percentage']=dealslist[0].percentage
                        data.append(details)
            else:
                details['special_offer']='0'
                data.append(details)
        
              
         getvals = operator.itemgetter('upload_name')
         data.sort(key=getvals)
         result = []        
         for k, g in itertools.groupby(data, getvals):
            result.append(g.next())
         #print result
         #keyfunc = lambda d: (d['upload_name'])
         #giter = groupby(sorted(data, key=keyfunc), keyfunc)
         #product = [g[1].next() for g in giter]        
         #args = request.args['upload_subcategory']
         log.info('Display the newarrivals')
         data=[]
         invalid_list=Sup_Upload.objects(upload_category__ne="Deals",status='Accept').filter(prices__doubleoffer_price__gt=0.0).order_by('-id')[0:10]
         for invalid_info in invalid_list:
            details={}
            details['avgrating']=invalid_info.avgrating
            details['upload_name']=invalid_info.upload_name
            details['upload_brand']=invalid_info.upload_brand
            details['upload_subcategory']=invalid_info.upload_subcategory
            details['upload_category']=invalid_info.upload_category
            details['upload_photo']=invalid_info.upload_photo
            details['extraimages']=invalid_info.extraimages
            attr_data=[]
            for attr in invalid_info.attributes:
                attr_details={}
                attr_details['atrname']=attr.atrname
                attr_details['atrvalue']=attr.atrvalue
                attr_data.append(attr_details)
            details['attributes']=attr_data
            for price in invalid_info.prices:
                details['doubleoffer_price']=price.doubleoffer_price
                details['offer_price']=price.offer_price
                details['enduser_price']=price.enduser_price
                details['percentage']=price.percentage
                
                
            dealslist = invalid_info.todaydeals
            if len(dealslist)>0:
                if dealslist[0].status=='True':
                        details['special_offer']=dealslist[0].special_discount
                        details['special_percentage']=dealslist[0].percentage
                        data.append(details)
            else:
                details['special_offer']='0'
                data.append(details)
                
         keyfunc = lambda d: (d['upload_name'])
         giter = groupby(sorted(data, key=keyfunc), keyfunc)
         product = [g[1].next() for g in giter]       
         coupons=[]         
         for coupon in OrderCoupons.objects(status="Active"):
            edate=datetime.datetime.strptime(coupon.end_date, '%d/%m/%Y')
            enddate= edate.date()
            fdate=datetime.datetime.strptime(coupon.from_date, '%d/%m/%Y')
            fromdate= fdate.date()
            if fromdate<=enddate:
                 discount=str(coupon.discount)+str(coupon.typef)
                 details={}
                 details['coupon_name']=coupon.coupon_name
                 details['coupon_code']=coupon.coupon_code
                 details['imageurl']=coupon.imageurl
                 details['discount']=discount
                 details['end_date']=coupon.end_date
                 #json_info=json.loads(json.dumps(details))
                 coupons.append(details)
         return {'baner':baner,'status':'Success','topbrands':topbrands,'collections':collections,'emergingbrands':emergingbrands,"deals":deals,'coupons':coupons,"offerscats":result,"newarrivalcats":product}


class MobileOffersCat(Resource):
    def get(self):
       if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
         args = request.args['upload_subcategory']
         #print args,"ram"
         data=[]
         invalid_list=Sup_Upload.objects(upload_category__ne="Deals",upload_subcategory__icontains=args,status='Accept').filter(prices__doubleoffer_price__gt=0.0).order_by('-prices.percentage')[0:10]
         #(Q(snapshot_values__key__in=key_list) & Q(snapshot_values__value__in=value_list).order_by('-todaydeals.percentage')
         '''
         for dealslist in invalid_list.todaydeals:
             if len(dealslist)>0:
                 print "if"
                 dealslist.order_by('-todaydeals.percentage')
             else:
                 print "else"
                 dealslist.order_by('-prices.percentage')
         '''        
         for invalid_info in invalid_list:
                details={}
                details['avgrating']=invalid_info.avgrating
                details['upload_name']=invalid_info.upload_name
                details['upload_brand']=invalid_info.upload_brand
                details['upload_subcategory']=invalid_info.upload_subcategory
                details['upload_category']=invalid_info.upload_category
                details['upload_photo']=invalid_info.upload_photo
                details['extraimages']=invalid_info.extraimages
                attr_data=[]
                for attr in invalid_info.attributes:
                    attr_details={}
                    attr_details['atrname']=attr.atrname
                    attr_details['atrvalue']=attr.atrvalue
                    attr_data.append(attr_details)
                details['attributes']=attr_data
                for price in invalid_info.prices:
                    details['doubleoffer_price']=price.doubleoffer_price
                    details['offer_price']=price.offer_price
                    details['enduser_price']=price.enduser_price
                    details['percentage']=price.percentage
                dealslist = invalid_info.todaydeals
                if len(dealslist)>0:
                    if dealslist[0].status=='True':
                            details['special_offer']=dealslist[0].special_discount
                            details['special_percentage']=dealslist[0].percentage
                            data.append(details)
                else:
                    details['special_offer']='0'
                    data.append(details)
                        
                    
         keyfunc = lambda d: (d['upload_name'])
         giter = groupby(sorted(data, key=keyfunc), keyfunc)
         product = [g[1].next() for g in giter]          
         
         log.info('Display the offers')
         return {'status':'Success','offerscats':product}
         
class MobileNewArrivalCat(Resource):
    def get(self):
       if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
         args = request.args['upload_subcategory']
         #print args,"sai"
         data=[]
         invalid_list=Sup_Upload.objects(upload_category__ne="Deals",upload_subcategory__icontains=args,status='Accept').filter(prices__doubleoffer_price__gt=0.0).order_by('-id')[0:10]
         for invalid_info in invalid_list:
                details={}
                details['avgrating']=invalid_info.avgrating
                details['upload_name']=invalid_info.upload_name
                details['upload_brand']=invalid_info.upload_brand
                details['upload_subcategory']=invalid_info.upload_subcategory
                details['upload_category']=invalid_info.upload_category
                details['upload_photo']=invalid_info.upload_photo
                details['extraimages']=invalid_info.extraimages
                attr_data=[]
                for attr in invalid_info.attributes:
                    attr_details={}
                    attr_details['atrname']=attr.atrname
                    attr_details['atrvalue']=attr.atrvalue
                    attr_data.append(attr_details)
                details['attributes']=attr_data
                for price in invalid_info.prices:
                    details['doubleoffer_price']=price.doubleoffer_price
                    details['offer_price']=price.offer_price
                    details['enduser_price']=price.enduser_price
                    details['percentage']=price.percentage
                    
                dealslist = invalid_info.todaydeals
                if len(dealslist)>0:
                    if dealslist[0].status=='True':
                            details['special_offer']=dealslist[0].special_discount
                            details['special_percentage']=dealslist[0].percentage
                            data.append(details)
                else:
                    details['special_offer']='0'
                    data.append(details)
         keyfunc = lambda d: (d['upload_name'])
         giter = groupby(sorted(data, key=keyfunc), keyfunc)
         product = [g[1].next() for g in giter]                   
         return {'status':'Success','newarrivalcats':product}

class MobileOffersCatAll(Resource):
    def get(self):
       if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
    
             data=[]
             invalid_list=Sup_Upload.objects(status='Accept').filter(prices__doubleoffer_price__gt=0.0).order_by('-prices.percentage')
             #print invalid_list,"list"
             #(Q(snapshot_values__key__in=key_list) & Q(snapshot_values__value__in=value_list).order_by('-todaydeals.percentage')
             '''
             for dealslist in invalid_list.todaydeals:
                 if len(dealslist)>0:
                     print "if"
                     dealslist.order_by('-todaydeals.percentage')
                 else:
                     print "else"
                     dealslist.order_by('-prices.percentage')
             '''        
             for invalid_info in invalid_list:
                    details={}
                    details['avgrating']=invalid_info.avgrating
                    details['upload_name']=invalid_info.upload_name
                    details['upload_brand']=invalid_info.upload_brand
                    details['upload_subcategory']=invalid_info.upload_subcategory
                    details['upload_category']=invalid_info.upload_category
                    details['upload_photo']=invalid_info.extraimages[0]
                    #details['extraimages']=invalid_info.extraimages
                    
                    attr_data=[]
                    for attr in invalid_info.attributes:
                        attr_details={}
                        attr_details['atrname']=attr.atrname
                        attr_details['atrvalue']=attr.atrvalue
                        attr_data.append(attr_details)
                    details['attributes']=attr_data
                    for price in invalid_info.prices:
                        details['doubleoffer_price']=price.doubleoffer_price
                        details['offer_price']=price.offer_price
                        details['enduser_price']=price.enduser_price
                        details['percentage']=price.percentage
                    dealslist = invalid_info.todaydeals
                    if len(dealslist)>0:
                        if dealslist[0].status=='True':
                                details['special_offer']=dealslist[0].special_discount
                                details['special_percentage']=dealslist[0].percentage
                                data.append(details)
                    else:
                        details['special_offer']='0'
                        data.append(details)
                            
                        
             keyfunc = lambda d: (d['upload_name'])
             giter = groupby(sorted(data, key=keyfunc), keyfunc)
             product = [g[1].next() for g in giter]          
             
             log.info('Display the offers')
             return {'status':'Success','offerscats':product}
        
         
class MobileNewArrivalCatAll(Resource):
    def get(self):
       if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
         #args = request.args['upload_subcategory']
         #print args,"args"
             data=[]
             invalid_list=Sup_Upload.objects(status='Accept').filter(prices__doubleoffer_price__gt=0.0).order_by('-id')
             for invalid_info in invalid_list:
                    details={}
                    details['avgrating']=invalid_info.avgrating
                    details['upload_name']=invalid_info.upload_name
                    details['upload_brand']=invalid_info.upload_brand
                    details['upload_subcategory']=invalid_info.upload_subcategory
                    details['upload_category']=invalid_info.upload_category
                    details['upload_photo']=invalid_info.extraimages[0]
                    attr_data=[]
                    for attr in invalid_info.attributes:
                        attr_details={}
                        attr_details['atrname']=attr.atrname
                        attr_details['atrvalue']=attr.atrvalue
                        attr_data.append(attr_details)
                    details['attributes']=attr_data
                    for price in invalid_info.prices:
                        details['doubleoffer_price']=price.doubleoffer_price
                        details['offer_price']=price.offer_price
                        details['enduser_price']=price.enduser_price
                        details['percentage']=price.percentage
                        
                    dealslist = invalid_info.todaydeals
                    if len(dealslist)>0:
                        if dealslist[0].status=='True':
                                details['special_offer']=dealslist[0].special_discount
                                details['special_percentage']=dealslist[0].percentage
                                data.append(details)
                    else:
                        details['special_offer']='0'
                        data.append(details)
             keyfunc = lambda d: (d['upload_name'])
             giter = groupby(sorted(data, key=keyfunc), keyfunc)
             product = [g[1].next() for g in giter]                   
             return {'status':'Success','newarrivalcats':product}
                   
'''                 
def send_async_sms(msg,mobile): 
    url = "http://www.smscountry.com/smscwebservice_bulk.aspx"
    values = {'user': 'powertex',
                  'passwd': 'PwRtx2018gsT',
                  'message': message,
                  'mobilenumber': number,
                  'mtype': 'N',
                  'DR': 'Y'
                  }
    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8')
    f = urllib.urlopen(url, data)
    #print f.read().decode('utf-8')

def SMS(message,mobile):
    mobilestr=""
    for mob in mobile:
        mobilestr=mobilestr+','+mob
    mobilestr.replace(' ,', '', 1)
    thr = Thread(target=send_async_sms, args=[message,mobilestr])
    thr.start()
'''   
    
class Test(Resource):
    def post(self):
       if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
           json_data = request.get_json(force=True)
           empid=json_data['empid']
           name=json_data['name']
           email=json_data['email']
           mobile='91'+json_data['mobile']
           qalification=json_data['qalification']
           ts=test(empid=empid,name=name,email=email,mobile=mobile,qalification=qalification)
           ts.save()
           return {"status":"success"}
    def get(self):
      if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
         brd=test.objects()
         topbrands = json.loads(brd.to_json())
         return {"status":"success","topbrands":topbrands}
    def put(self):
      if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
         json_data = request.get_json(force=True)
         empid=request.args['empid']
         brd=test.objects.get(empid=empid)
         brd.empid=json_data['empid']
         brd.name=json_data['name']
         brd.email=json_data['email']
         brd.mobile='91'+json_data['mobile']
         brd.qalification=json_data['qalification']
         brd.save()
         return {"status":"success"}

    def delete(self):
       if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
         empid=request.args['empid']
         exp=test.objects(empid=empid)
         exp.delete()
         return {"status":"success"}

        
class Test123(Resource):        
    def post(self):
       if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
           json_data = request.get_json(force=True)           
           fname=json_data['fname']
           lname=json_data['lname']
           gender=json_data['gender']
           email=json_data['email']
           mobile='91'+json_data['mobile']
           address=json_data['address']
           password=json_data['password']
           cnfrmPwd=json_data['cnfrmPwd']
           ts=reg(fname=fname,lname=lname,gender=gender,email=email,mobile=mobile,address=address,password=password,cnfrmPwd=cnfrmPwd)
           ts.save()
           return {"status":"success"}
    def get(self):
           user=request.args['username']
           password = request.args['password']
           regs=[]
           id_1=''
           if '@' in user:
               inf=reg.objects.get(email=user)
               if inf.password==password:
                   status='success'
                   data={}
                   data['email']=inf.email
                   data['password']=inf.password
                   id_1=str(inf.id)
                   regs.append(data)
                   print(data)
                   regd = json.loads(json.dumps(regs))
               else:
                   status='fail'
                   regd={'error':'wrong password'}
           else:
               inf=reg.objects.get(mobile=user,password=password)
               status='success'
               data={}
               data['mobile']=inf.mobile
               data['password']=inf.password
               id_1=str(inf.id)
               regs.append(data) 
               regd = json.loads(json.dumps(regs))
           return {"status":status,"regd":regd,'id':id_1}
          


class LogOut(Resource):
    def post(self):
        if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
            json_data = request.get_json(force=True)
            token = json_data['token']
            user = reg.objects.get(id=token)
            user.id=token
            user.save()
            return {"status":"success","message":"record deleted successfully"}
        else:
            return {"status":"invalid secret key"}

class ForgotPassword(Resource):
    def post(self):
        if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
            json_data = request.get_json(force=True)
            username=json_data['username']
            if '@' in username:
                registeredUser = reg.objects(email=username)
                my_secret = 'MFRGGZDFMZTWQ2LK'
                otp_is = otp.get_totp(my_secret)
                if registeredUser.count()>0:
                        user_info = reg.objects.get(email=username)
                        user_info.otp = str(otp_is)
                        user_info.save()
                        msg = 'Your one time password is ' + str(otp_is)
                        #mobile = '91' + username
                        #SMS(msg, mobile)
                return {"status":"success","otp":msg}
            else:
                registeredUser1 = reg.objects(mobile=username)
                my_secret = 'MFRGGZDFMZTWQ2LK'
                otp_is = otp.get_totp(my_secret)
                if registeredUser1.count()>0:
                        user_info = reg.objects.get(mobile=username)
                        user_info.otp = str(otp_is)
                        user_info.save()
                        msg = 'Your one time password is ' + str(otp_is)
                        #mobile = '91' + username
                        #SMS(msg, mobile)
                        
                return {"status":"success","otp":msg}
    def get(self):
                args = request.args
                req_mobile=args['username']
                req_otp=args['otp']
                user_info = reg.objects(mobile=req_mobile,otp=req_otp)
                '''
                if user_info.count() == 0:
                    return {"status":"invalid OTP"}'''

                return {"status":"success"}


class ResetPassword(Resource):
    def post(self):
        if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
            json_data = request.get_json(force=True)
            userid=json_data['username']
            new_password=json_data['new_password']
            confirm_password=json_data['confirm_password']
            user_info = reg.objects.get(email=userid)
            if new_password == confirm_password: 
                new_pwd = new_password
                user_info.password=new_pwd
                user_info.save()
                return {"status":"password changed successfully"}
            else:
                return {"status":"new_password and confirm_password doesnot matched"}
        else:
            return {"status":"invalid secret key"}

class Allategories(Resource):
    def get(self):
        if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
            categories=Category.objects()
            data=[]
            for cat in categories:
                sup=Sup_Upload.objects(upload_category=cat.categoryname) 
                if sup.count()>0:
                    details={}
                    details['categoryname']=cat.categoryname
                    sub_data=[]
                    for subcat in Sub_Category.objects(categoryname=cat.categoryname):
                        sup=Sup_Upload.objects(upload_subcategory=subcat.subcategory)
                        if sup.count()>0: 
                            sub_cat={}
                            sub_cat['subcategory']=subcat.subcategory
                            sub_cat['modelno']=sup[0].upload_modelno
                            sub_cat['name']=sup[0].upload_name
                            sub_cat['image']=sup[0].upload_photo
                            sub_cat['upload_discount']=sup[0].upload_discount
                            sub_cat['upload_mrp']=sup[0].upload_mrp
                            sub_cat['upload_netPrice']=sup[0].upload_netPrice
                            
                            json_sub_cat=json.loads(json.dumps(sub_cat))
                            sub_data.append(json_sub_cat)
                            #sub_cat=sorted(sub_data)
                            
                    details['subcategoryname']=sub_data
                    json_cat=json.loads(json.dumps(details))
                    data.append(json_cat)
            return {"status":"success","categories":data}

class Categories(Resource):
    def get(self):
        if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
            cate=request.args['param_other1']
            categories=Category.objects(categoryname=cate)
            data=[]
            for cat in categories:
                sup=Sup_Upload.objects(upload_category=cat.categoryname) 
                if sup.count()>0:
                    details={}
                    details['categoryname']=cat.categoryname
                    sub_data=[]
                    for subcat in Sub_Category.objects(categoryname=cat.categoryname):
                        sup=Sup_Upload.objects(upload_subcategory=subcat.subcategory)
                        if sup.count()>0: 
                            sub_cat={}
                            sub_cat['subcategory']=subcat.subcategory
                            sub_cat['modelno']=sup[0].upload_modelno
                            sub_cat['name']=sup[0].upload_name
                            sub_cat['image']=sup[0].upload_photo
                            sub_cat['upload_discount']=sup[0].upload_discount
                            sub_cat['upload_mrp']=sup[0].upload_mrp
                            sub_cat['upload_netPrice']=sup[0].upload_netPrice
                            
                            json_sub_cat=json.loads(json.dumps(sub_cat))
                            sub_data.append(json_sub_cat)
                            #sub_cat=sorted(sub_data)
                            
                    details['subcategoryname']=sub_data
                    json_cat=json.loads(json.dumps(details))
                    data.append(json_cat)
            return {"status":"success","categories":data}

class Catsubcat(Resource):
    def get(self):
        if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
            cate=request.args['param_other1']
            sub=request.args['param_other2']
            data=[]
            sub_data=[]
            for subcat in Sub_Category.objects(categoryname=cate,subcategory=sub):
                sup=Sup_Upload.objects(upload_subcategory=subcat.subcategory)
                details={}
                if sup.count()>0: 
                    sub_cat={}
                    sub_cat['subcategory']=subcat.subcategory
                    sub_cat['modelno']=sup[0].upload_modelno
                    sub_cat['name']=sup[0].upload_name
                    sub_cat['image']=sup[0].upload_photo
                    sub_cat['upload_discount']=sup[0].upload_discount
                    sub_cat['upload_mrp']=sup[0].upload_mrp
                    sub_cat['upload_netPrice']=sup[0].upload_netPrice
                    json_sub_cat=json.loads(json.dumps(sub_cat))
                    sub_data.append(json_sub_cat)            
            details['subcategoryname']=sub_data
            json_cat=json.loads(json.dumps(details))
            data.append(json_cat)
            return {"status":"success","categories":json_cat}


class productDetail(Resource):
    def post(self):
         if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
            json_data = request.get_json(force=True)
            print(json_data)
            username=json_data['username']
            print(username)
            category=json_data['subcategory']
            print(category)
            subcategory=json_data['name']
            modelno=json_data['modelno']
            image=json_data['image']
            upload_mrp=json_data['upload_mrp']
            upload_discount=json_data['upload_discount']
            upload_netPrice=json_data['upload_netPrice']
            #print(username)
            ts=addtocart(username=username,category=category,subcategory=subcategory,modelno=modelno,image=image,upload_mrp=upload_mrp,upload_discount=upload_discount,upload_netPrice=upload_netPrice)
            ts.save()
            return {"status":"success","data":json_data}

    def get(self):
        if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
            user=request.args['param_other1']
            addtocartget=addtocart.objects(username=user)
            si=[]
            for i in addtocartget:
                se={}
                se['username']=i.username
                se['subcategory']=i.subcategory
                se['modelno']=i.modelno
                se['image']=i.image
                se['upload_mrp']=i.upload_mrp
                se['upload_discount']=i.upload_discount
                se['upload_netPrice']=i.upload_netPrice
            si.append(se)
            return {"status":"success","data":si}


class AddToCartSite(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        user_id=json_data['user_id']
        #req_randomnumber=json_data['random_no'] if 'random_no' in json_data else ''       
        model =json_data['modelNo']
        supp_product=Sup_Upload.objects(upload_modelno=model).only('upload_tax','upload_id','prices','upload_subcategory','upload_brand','upload_mrp','end_user_disc')
        for ofrprice in supp_product:
                tax=ofrprice.upload_tax
                upload_photo='011'+ofrprice.upload_id+'.jpg'
                image=upload_photo
                subcategory=ofrprice.upload_subcategory
                brand=ofrprice.upload_brand
                offer_price = ofrprice.upload_mrp
                offer_price_gst=ofrprice.upload_mrp
                order_details=OrderitemsSite(productdescription,qty,offer_price,offer_price_gst,tax,image,subcategory,brand)
                customer_order.orderitemsite.append(order_details)
                customer_order.save()
        return {"status":"item added to cart"}

    def get(self):
        if request.headers.has_key('secret_key') and request.headers['secret_key']==secret_key:
            user=request.args['param_other1']
            addtocartget=addtocart.objects(username=user)
            si=[]
            for i in addtocartget:
                se={}
                se['username']=i.username
                se['subcategory']=i.subcategory
                se['modelno']=i.modelno
                se['image']=i.image
                se['upload_mrp']=i.upload_mrp
                se['upload_discount']=i.upload_discount
                se['upload_netPrice']=i.upload_netPrice
            si.append(se)
            return {"status":"success","data":si}

        


       

        
       
        
           
 

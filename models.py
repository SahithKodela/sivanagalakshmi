#!/usr/bin/env python2.7
from mongoengine import connect,DynamicDocument
from mongoengine.fields import *
import datetime
#import config
from mongoengine import Document, EmbeddedDocument, StringField, DateTimeField, EmbeddedDocumentField, ListField
from werkzeug.security import  check_password_hash,generate_password_hash


#connect('qa-hub', host='192.168.20.40', port=27017, username='qahub1', password='qapro1@goldensun')
#connect('testsmthub', host='192.168.20.39', port=27017, username='testsmthubuser', password='testsmt@smthub')
connect('hub-smt', host='192.168.20.6', port=27017, username='gsthub1', password='hubgst1@goldensun')
#connect('Hub-smt', host='192.168.20.52', port=27017, username='', password='')
#connect('productiondb',host='157.119.108.133', port=27017,username='prohub',password='prohub@6199')

class UserSignup(DynamicDocument):
     username = StringField()
     email = EmailField()
     mobile = StringField()
     password = StringField()
     usertype = StringField()
     registered_on = DateTimeField( "Date",format="%Y-%m-%d",default=datetime.date.today())
     status = StringField(default='Inactive')
     userid = StringField(default='None')
     lastlogin=DateTimeField( "Dates",default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
     login_attempts=StringField(default='0')
     def is_authenticated(self):
        return True

     def is_active(self):
        return True

     def is_anonymous(self): 
        return False

     def get_id(self):
          
        return unicode(self.id)

     def __repr__(self):
        return '<User %r>' % (self.username)


class atr1(EmbeddedDocument):
    atrname = StringField()
    atrvalue = StringField()
    tolerance1 =StringField()
    tolerance2=StringField()
    
class Sup_Upload1(DynamicDocument):
     #user_id=StringField()
     upload_id = StringField()
     upload_category = StringField()
     #oem_code=StringField()
     upload_subcategory = StringField()
     upload_name= StringField()
     upload_modelno= StringField()
     upload_brand = StringField()
     upload_warranty= StringField()
     upload_pieceperCarton = StringField()
     STD_non_pack=StringField()
     upload_minimumOrder = StringField()
     upload_netWeight=StringField()
     upload_mrp = StringField()
     upload_price=StringField()
     discount=StringField()
     upload_discount=StringField()
     tax=StringField()
     upload_tax=StringField()
     upload_netPrice=StringField()
     upload_hsncode=StringField()
     upload_locations=StringField()
     frequency=StringField()
     remarks=StringField()
     salesqty=StringField()
     description=StringField()
     #extraimages=ListField()
     avgrating=StringField()
     manual_video=StringField()
     manual_pdf=StringField()
     lastweeksales=StringField()
     created_date = DateTimeField( "created_date",format="%d/%m/%y",default=datetime.datetime.now)
     searchterm=StringField()
     sup_claim=StringField()
     qc_remarks=StringField()
     cust_advantages=StringField()
     spar_upload_id=StringField()
     altr_upload_id=StringField()
     avg_volume=StringField()
     prod_movment=StringField()
     prod_rating=StringField()
     new_arrival_sno=StringField()
     key_features=StringField()
     prod_functions=StringField()
     landing_price=StringField()
     MRP=StringField()
     dealer_a_disc=StringField()
     dealer_b_disc=StringField()
     dealer_c_disc=StringField()
     dealer_d_disc=StringField()
     dealer_e_disc=StringField()
     end_user_disc=StringField()
     vendor_code=StringField()
     wh_qty=StringField()
     attributes = ListField(EmbeddedDocumentField(atr1))     


def userLoginCheck(loginid,formPassword):
    try:
     if '@' in loginid:
          
          dbUser = UserSignup.objects(email=loginid)
          if dbUser.count()==0:
               return "Fail"
          
          dbPassword = str(dbUser[0].password)
          if check_password_hash(dbPassword,formPassword):
               return dbUser[0]
          else:
               return "Fail"
          
     else:
          dbUser = UserSignup.objects(mobile=loginid)
          if dbUser.count()==0:
               return "Fail"
          dbPassword = str(dbUser[0].password)
          if check_password_hash(dbPassword,formPassword):
               return dbUser[0]
          else:
               return "Fail"
    except Exception as e:
        return str(e)

def userLoginCheck1(email,formPassword):
    try:
          dbUser = UserSignup.objects(email=email)
          if dbUser.count()==0:
               return "Fail"
          
          dbPassword = str(dbUser[0].password)
          if check_password_hash(dbPassword,formPassword):
               return dbUser[0]
          else:
               return "Fail"  

    except Exception as e:
        return str(e)

class Usertype(DynamicDocument):
     usertype=StringField()
     userrole=StringField()
#-----------------------------------------------------Reg Forms--------------------------------
     
class Reg_Dealer(DynamicDocument):
     user_id=StringField()
     dealer_name = StringField()
     dealer_shopname=StringField()
     dealer_cin = StringField()
     dealer_address = StringField()
     dealer_country= StringField()
     dealer_state= StringField()
     dealer_city = StringField()
     dealer_town= StringField()
     dealer_pin = StringField()
     dealer_phone = StringField()
     dealer_mail = EmailField()
     dealer_gstin=StringField()
     dealer_pan=StringField()
     #contact person
     dealer_contactname=StringField()
     dealer_mobile=StringField()
     dealer_email=EmailField()

class Goods(EmbeddedDocument):
    supplier_brand = StringField()
    supplier_tm = StringField()   
       

class Reg_Supplier(DynamicDocument):
     user_id=StringField()
     supplier_name = StringField()
     supplier_companyname = StringField()
     supplier_cin = StringField()
     supplier_address = StringField()
     supplier_country= StringField()
     supplier_state= StringField()
     supplier_city = StringField()
     supplier_town= StringField()
     supplier_pin = StringField()
     supplier_phone = StringField()
     supplier_mail = EmailField()
     supplier_gstin=StringField()
     supplier_pan=StringField()
     supplier_brands = ListField(EmbeddedDocumentField(Goods))
     #contact person
     supplier_contactname=StringField()
     supplier_mobile=StringField()
     supplier_email=EmailField()
     supplier_id=StringField()
     
class Reg_Service(DynamicDocument):
     user_id=StringField()
     service_name = StringField() 
     service_cin= StringField()
     service_address= StringField()
     service_country = StringField()
     service_state = StringField()
     service_city = StringField()
     service_town = StringField()
     service_landmark = StringField()
     service_pin = StringField()
     service_phone = StringField()
     service_mail = EmailField()
     service_pan = StringField()
     service_tin = StringField()
     service_contactname = StringField()
     service_mobile = StringField()
     service_email = EmailField()

class Reg_Contractor(DynamicDocument):
     user_id=StringField()
     contractor_name = StringField() 
     contractor_cin= StringField() 
     contractor_address = StringField() 
     contractor_country = StringField() 
     contractor_state = StringField() 
     contractor_city = StringField() 
     contractor_town = StringField() 
     contractor_pin = StringField() 
     contractor_phone = StringField() 
     contractor_pan = StringField() 
     contractor_tin = StringField() 
     contractor_mail = EmailField()
     contractor_worklocation = StringField() 
     contractor_areaofwork = StringField() 
     contractor_workperiod = StringField() 
     contractor_contactname = StringField() 
     contractor_mobile = StringField() 
     contractor_email =  EmailField()
     
#--------------------------------------master product-------------------     
class Category(DynamicDocument):
     categoryid = StringField() 
     categoryname= StringField() 

class Sub_Category(DynamicDocument):
     categoryname = StringField()
     subcategoryid= StringField()
     subcategory= StringField()

class Atname(EmbeddedDocument):
    atrname = StringField()     

class Product(DynamicDocument):
     productid = StringField()
     categoryname = StringField()
     subcategory= StringField()
     productname= StringField()
     description=StringField()
     attribute = ListField(EmbeddedDocumentField(Atname))


'''class Attributes(DynamicDocument):
     categoryname = StringField()
     subcategory= StringField()
     productname= StringField()
     attribute = ListField(EmbeddedDocumentField(Atname))'''
     
#---------------------------------------------supplier------------------------/shopuser------------------------------    
class TodayDeals(EmbeddedDocument):
     productid=StringField()
     fromdate=DateTimeField()
     todate=DateTimeField()
     mrp=FloatField()
     special_discount=FloatField()
     special_discount_gst=FloatField()
     percentage = FloatField()
     flagfield=StringField(default='Enable')
     status=StringField(default='True')
     
class atr(EmbeddedDocument):
    atrname = StringField()
    atrvalue = StringField()

  
class PriceLists(EmbeddedDocument):
     landing_price=StringField()
     dealer_price=StringField()
     offer_price=StringField()
     enduser_price=StringField()
     bulk_unit_price = StringField()
     bulk_qty=StringField()
     doubleoffer_price=FloatField()
     percentage=FloatField()
     landing_price_gst=FloatField()
     dealer_price_gst=FloatField()
     offer_price_gst=FloatField()
     enduser_price_gst=FloatField()

class Sup_Upload(DynamicDocument):
     user_id=StringField()
     upload_id = StringField()
     upload_category = StringField()
     upload_subcategory = StringField()
     upload_name= StringField()
     upload_modelno= StringField()
     upload_brand = StringField()
     upload_warranty= StringField()
     upload_pieceperCarton = StringField()
     upload_minimumOrder = StringField()
     upload_netWeight=StringField()
     upload_mrp = StringField()
     upload_price=StringField()
     discount=StringField()
     upload_discount=StringField()
     tax=StringField()
     upload_tax=StringField()
     upload_netPrice=StringField()
     upload_hsncode=StringField()
     upload_locations=StringField()
     frequency=StringField()
     upload_photo=StringField()
     attributes = ListField(EmbeddedDocumentField(atr))
     prices=ListField(EmbeddedDocumentField(PriceLists))
     status = StringField(default='Inprocess')
     remarks=StringField()
     salesqty=StringField()
     description=StringField()
     extraimages=ListField()
     avgrating=StringField()
     manual_video=StringField()
     manual_pdf=StringField()
     lastweeksales=StringField()
     extraimages=ListField()
     tags=ListField()
     metadescription=ListField()
     keywords=ListField()
     todaydeals=ListField(EmbeddedDocumentField(TodayDeals))
     search_keywords=ListField()
     productid=StringField()
     created_date = DateTimeField( "created_date",format="%d/%m/%y",default=datetime.datetime.now)
     '''
     meta = {'indexes': [
        {'fields': ['$upload_name', "$description","$upload_brand","$upload_category","$upload_subcategory"],
         'default_language': 'english',
         'weights': {'upload_name': 1, 'description': 2, 'upload_brand': 3, 'upload_category': 4, 'upload_subcategory': 5}
        }
    ]}
     '''
class Shipping_Setup(DynamicDocument):
     user_id=StringField()
     vehiclenumber=StringField()
     drivername = StringField()
     contactnumber = StringField()
     alternativecontact = StringField()

class Supplier_Tax(DynamicDocument):
     user_id=StringField()
     taxId=StringField()
     taxName = StringField()
     taxRate = StringField()

class Supplier_Discount(DynamicDocument):
     user_id=StringField()
     discountId=StringField()
     discountName = StringField()
     discountRate = StringField()
     
#---------------------------------------------------WH Form----------------------
class Warehouse(DynamicDocument):
     user_id=StringField()
     warehouse_id=StringField()
     warehouse_name = StringField()
     warehouse_address = StringField()
     warehouse_email = StringField()
     warehouse_phone = StringField()
     #warehouse_password = StringField()
     warehouse_manager=StringField()
     
#------------------------------------------------------------------------ Barcode -----------------------------------
         
class Barcode_Info(DynamicDocument):
     barcode_id=StringField()
     barcode_type = StringField()
     generated_date = StringField()

class Carton(EmbeddedDocument):
    barcode = StringField()
   
    
class BarCode_Carton(DynamicDocument):
     mainbarcode=StringField()
     barcodelist=ListField(EmbeddedDocumentField(Carton))


class LatestBarcode(DynamicDocument):
     barcode = StringField()


#----------------------------------------------------Purchase Orders----------------------------------------

class LatestPurchasecode(DynamicDocument):
     purchasecode = StringField()	 

class WHOrders(EmbeddedDocument):
    items = StringField()
    order_id = StringField()
    name=StringField()
    model_no= StringField()
    hsn=StringField()
    quantity = StringField()
    netprice = StringField()
    value= StringField()
                
class PurchaseOrders(DynamicDocument):
     user_id=StringField()
     warehouse_name = StringField()
     supplier_name = StringField()
     supplier_id = StringField()
     supplier_address = StringField()
     purchaseManager = StringField()
     purchaseOrder_no = StringField()
     po_date = StringField()
     orderslist=ListField(EmbeddedDocumentField(WHOrders))
     totalitems=StringField()
     totalqty=StringField()
     totalvalue=StringField()
     status = StringField(default='Pending')
     remarks=StringField()
     created_date = DateTimeField( "created_date",format="%d/%m/%y",default=datetime.datetime.now)

class CatSubAtr(DynamicDocument):
     user_id=StringField()
     category = StringField()
     subcategory = StringField()
     attributes = StringField()
     
     
class Invoice(EmbeddedDocument):
     items = StringField()
     item_id= StringField()
     item_model = StringField()
     item_quntity = StringField()
     item_price = StringField()
     item_value = StringField()

class Charges(EmbeddedDocument):
     charge_name = StringField()
     charge_value = StringField()
class BankDetail(EmbeddedDocument):
     ac_holdername=StringField()
     bankac_number=StringField()     
     ac_type=StringField()
     ifsc_code = StringField()
     micr_code = StringField()
	 
class PurchaseInvoice(DynamicDocument):
     user_id=StringField()
     ware_house=StringField()
     supplier_id = StringField()
     purchase_manager_id=StringField()
     purchaseOrder_no=StringField()
     supplier_gstno = StringField()
     invoice_no=StringField()
     invoice_date=StringField()
     expected_date=StringField()
     invoice=ListField(EmbeddedDocumentField(Invoice))
     bankdetails= ListField(EmbeddedDocumentField(BankDetail))
     #shipping_charges  = StringField()
     othercharges=ListField(EmbeddedDocumentField(Charges))
     total_items= StringField()
     total_qty = StringField()
     total_value = StringField()
     status = StringField(default='Process')
     remarks=StringField()
     shipping_barcode=StringField()
     created_date = DateTimeField( "created_date",format="%d/%m/%y",default=datetime.datetime.now)
     
class LatestInvoicecode(DynamicDocument):
     invoiceCode = StringField()
     
#------------------------------------------------------------ Shop Orders------------------------------------------     

class ShopUser(DynamicDocument):
     user_id=StringField()
     userid=StringField()
     username=StringField()
     email=StringField()
     mobile=StringField()
     shop=StringField()
     password=StringField()
     createdby=StringField()
     created_date=StringField()
     
class Shopsetup(DynamicDocument):
     user_id=StringField()
     shop_id =StringField()
     shop_name=StringField()
     shop_address=StringField()
     pincode=StringField()
     lat_long=PointField(auto_index=True)
     email = StringField()
     phone = StringField()
     dealer=StringField()
     password = StringField()


class LatestShopPurchasecode(DynamicDocument):
     purchasecode = StringField()
     
class Orders(EmbeddedDocument):
    items = StringField()
    supplier= StringField()
    model_no= StringField()
    hsn = StringField()
    quantity = StringField()
    netprice = StringField()
    value= StringField()
                
                
class ShopOrders(DynamicDocument):
     user_id=StringField()
     warehouse_name = StringField()
     shop_name = StringField()
     shop_id = StringField()
     shop_address = StringField()
     dealer_id = StringField()
     shop_purchaseorderno = StringField()
     po_date = StringField()
     orderslist=ListField(EmbeddedDocumentField(Orders))
     totalitems=StringField()
     totalqty=StringField()
     totalvalue=StringField()
     status = StringField(default='Pending')
     remarks=StringField()
     created_date = DateTimeField( "created_date",format="%d/%m/%y",default=datetime.datetime.now)

class ShopInvoice(EmbeddedDocument):
     items = StringField()
     hsn= StringField()
     prod_desc= StringField()
     #order_id = StringField()
     model_no= StringField()
     quantity = StringField()
     mrp = StringField()
     #discount= StringField()
     netprice = StringField()
     tax= StringField()
     value = StringField()
     
class ShopCharges(EmbeddedDocument):
     charge_name = StringField()
     charge_value = StringField()


     
class ShopOrderInvoice(DynamicDocument):
     user_id=StringField()
     ware_house=StringField()
     shop_name = StringField()
     shop_id = StringField()
     dealer_id = StringField()
     shop_purchaseorderno = StringField()
     shopinvoice_number=StringField()
     invoice_date=StringField()
     expected_date=StringField()
     invoice=ListField(EmbeddedDocumentField(ShopInvoice))
     othercharges=ListField(EmbeddedDocumentField(ShopCharges))
     total_items= StringField()
     total_quantity = StringField()
     total_value = StringField()
     status = StringField(default='Accept')
     shipping_barcode=StringField()
     created_date = DateTimeField( "created_date",format="%d/%m/%y",default=datetime.datetime.now)
     
class LatestInvoicecode(DynamicDocument):
     invoiceCode = StringField()

class ProductInventory(EmbeddedDocument):
      model_number=StringField()
      hsn_number=StringField()
      avl_qty=StringField()
      soldout_qty=StringField()
      
class Wh_Inventory(DynamicDocument):
     whid=StringField()
     wh_inventory=ListField(EmbeddedDocumentField(ProductInventory))

class Shop_Inventory(DynamicDocument):
     shopid=StringField()
     shop_inventory=ListField(EmbeddedDocumentField(ProductInventory))


class Company_Setup(DynamicDocument):
     user_id=StringField()
     companyname=StringField()
     address = StringField()
     pan = StringField()
     gstin = StringField()
     cin=StringField()
     state=StringField()
     statecode=StringField()


class Billing_Setup(DynamicDocument):
     user_id=StringField()
     dealerid=StringField()
     companyname=StringField()
     address = StringField()
     pan = StringField()
     gstin = StringField()
     cin=StringField()
     state=StringField()
     statecode=StringField()    
     statecode=StringField()
     companylogo = StringField()
     contactno=StringField()
     
class Bank_Setup(DynamicDocument):
     user_id=StringField()
     bankac_number=StringField()
     ac_holdername=StringField()
     ac_type=StringField()
     bank_name = StringField()
     ifsc_code = StringField()
     micr_code = StringField()
     branch_name = StringField()
     branch_address=StringField()
     statecode=StringField()
     companylogo = StringField()
     contactno=StringField()

class Header_Setup(DynamicDocument):
     user_id=StringField()
     companyname=StringField()
     address = StringField()
     companylogo = StringField()
     contactno=StringField()
     

class Fair_Contact(DynamicDocument):
     username = StringField()
     email = StringField()
     business_type = StringField()  
     mobile_no = StringField()
     others = StringField()
     
class PriceList(EmbeddedDocument):
     landing_price=StringField()
     dealer_price=StringField()
     offer_price=StringField()
     enduser_price=StringField()
     landing_price_gst=FloatField()
     dealer_price_gst=FloatField()
     offer_price_gst=FloatField()
     enduser_price_gst=FloatField()
     bulk_unit_price = StringField()
     bulk_qty=StringField()


class InvoiceList(EmbeddedDocument):
     invoiceid=StringField()
     fromsmt=StringField()
     tosmt=StringField()
     invoicedate=StringField()
     

class ProdinvWH(DynamicDocument):
     user_id=StringField()
     supplier = StringField()
     warehouse = StringField()
     hsn=StringField()
     modelno = StringField()  
     brand = StringField()
     prod_desc = StringField()
     invoice_smtlist=ListField(EmbeddedDocumentField(InvoiceList))
     smtids=ListField()
     quantity=StringField()
     outqty=StringField()
     prices=ListField(EmbeddedDocumentField(PriceList))
     barcode=StringField()
     status=StringField(default='Not Print')
     created_date = DateTimeField( "created_date",format="%d/%m/%y",default=datetime.datetime.now)



class Latestsmtcode(DynamicDocument):
     SmtidCode = StringField()


class RandomCode(DynamicDocument):
     number = StringField()

class DealerRandomCode(DynamicDocument):
     number = StringField()  


class Prices(EmbeddedDocument):
     dealer_price=StringField()
     enduser_price=StringField()
     offer_price=StringField()
     comboffer=StringField()
     landing_price_gst=FloatField()
     dealer_price_gst=FloatField()
     offer_price_gst=FloatField()
     enduser_price_gst=FloatField()

class SmtidShop(EmbeddedDocument):
     smtid=ListField()
     invoiceid=StringField()

class ProdInvShop(DynamicDocument):
     user_id=StringField()
     supplier=StringField()
     warehouse=StringField()
     shop=StringField()
     model=StringField()
     brand=StringField()
     category=StringField()
     subcategory=StringField()
     price=ListField(EmbeddedDocumentField(Prices))
     smtidshop=ListField(EmbeddedDocumentField(SmtidShop))
     inqty=StringField()
     outqty=StringField()
     proddescription=StringField()
     image=StringField()
     avlsmtid=ListField()
     barcode=StringField()
     tax=StringField()
     status=StringField(default='Delivered')
     created_date = DateTimeField( "created_date",format="%d/%m/%y",default=datetime.datetime.now)

     
class Notifications(DynamicDocument):
     usertype=StringField()
     user_id=StringField()
     date_time=StringField()
     message=StringField()
     title=StringField()
     status=StringField()
     last_notification_time=StringField()

class UserOrderList(EmbeddedDocument):
      product_id=StringField()
      product_name=StringField()
      modelnumber=StringField()
      sku=StringField()
      price=StringField()
      offer_price=StringField()
      brand=StringField()
      quantity=StringField()
      
class UserOrders(DynamicDocument):
     order_created_date=StringField()
     order_id=StringField()
     customer_email=StringField()
     firstname=StringField()
     lastname=StringField()
     mobile=StringField()
     ordered_items=ListField(EmbeddedDocumentField(UserOrderList))
     shipping_address=StringField()
     billing_address=StringField()
     base_subtotal=StringField()
     shipping_amount=StringField()

class ShipData(EmbeddedDocument):
     items = StringField()
     model=StringField()
     brand=StringField()
     smtid=ListField()
     qty=StringField()
     
class ProdInvShipping(DynamicDocument):    
     warehouse=StringField()
     shop=StringField()
     invoice=StringField()
     startdate=StringField()
     orderslist=ListField(EmbeddedDocumentField(ShipData))
     receiptid=StringField()
     shippingdetails=StringField()
     remarks=StringField()
     status=StringField(default='Shipping')
     

class BillingShippingAddress(EmbeddedDocument):
     firstname=StringField()
     lastname=StringField()
     house_no=StringField()
     street_address = StringField()  
     city = StringField()
     state = StringField()  
     postal_code = StringField()
     country = StringField()
     mobile=StringField()
     alt_mobile=StringField()
     address_id=StringField()
     
class OrderItem(EmbeddedDocument):
     sno=StringField()
     productdescription=StringField()
     qty=StringField()
     unitprice=StringField()
     enduser_price=StringField()
     total=StringField()
     tax=StringField()
     tax_amount=StringField()
     sub_total=StringField()     
     
class Rating_UserToShop(EmbeddedDocument):
     rating=StringField()
     remarks=StringField()

     
class Rating_ShopToUser(EmbeddedDocument):
     rating=StringField()
     remarks=StringField()

class CouponInOrder(EmbeddedDocument):
     cupon_id=StringField()
     discount=StringField()

class CustomerOrders(DynamicDocument):
     orderid=StringField()
     createddate=StringField()
     lastupdateddate=StringField()
     status=StringField()
     shop=StringField()
     fromweb=StringField()
     customermobile=StringField()
     totalamount=StringField()
     invoiceid=StringField()
     orderitems=ListField(EmbeddedDocumentField(OrderItem))
     remarks=StringField()
     payment_status=StringField()
     shippingaddress=ListField(EmbeddedDocumentField(BillingShippingAddress))
     shippingtype=StringField()
     rating_usertoshop=ListField(EmbeddedDocumentField(Rating_UserToShop))
     rating_shoptouser=ListField(EmbeddedDocumentField(Rating_ShopToUser))
     totalquantity=StringField()
     paymenttype=StringField()
     verifycode=StringField()
     email=StringField()
     total_items=StringField()
     order_transfer=ListField()
     transactionid=StringField()
     discountAmount=StringField()
     order_settlement=BooleanField()
     settelmentAmount=StringField()
     billingaddress=ListField(EmbeddedDocumentField(BillingShippingAddress))
     cupon=ListField(EmbeddedDocumentField(CouponInOrder))
     created_date = DateTimeField( "created_date",format="%d/%m/%y",default=datetime.datetime.now)
     pic_alt_mobile=StringField()

class ShopRandomCode(DynamicDocument):
     number = StringField()

class ServiceTax(DynamicDocument):
     user_id=StringField()
     taxid=StringField()
     tax_name = StringField()
     tax_rate = StringField()     

class ConfirmInvoiceOrderItems(EmbeddedDocument):
     productdesp=StringField()
     smtids=ListField()
    
class ConfirmInvoice(DynamicDocument):
     orderid=StringField()
     invoiceid=StringField()
     shop=StringField()
     totalamount=StringField()
     createddate=StringField()
     paymenttype=StringField()
     user_mobile=StringField()
     orderitem=ListField(EmbeddedDocumentField(ConfirmInvoiceOrderItems))
     created_date = DateTimeField( "created_date",format="%d/%m/%y",default=datetime.datetime.now)

class ProdInfo(EmbeddedDocument):
     productdesp=StringField()
     smtids=ListField()
     invoiceid=StringField()
     
class CmrInfo(EmbeddedDocument):
     user=StringField()
     prodinfo=ListField(EmbeddedDocumentField(ProdInfo))
    

class ProdInvCMR(DynamicDocument):
     supplier=StringField()
     warehouse=StringField()
     shop=StringField()
     model=StringField()
     brand=StringField()
     cmrinfo=ListField(EmbeddedDocumentField(CmrInfo))
     created_date = DateTimeField( "created_date",format="%d/%m/%y",default=datetime.datetime.now)
     

class CustomerCoupon(EmbeddedDocument):
     coupon_id=StringField()
     createddate=StringField()
     value=StringField()
     coupon_type=StringField()
     maxvalue=StringField()
     status=StringField(default='True')
    
class CustomerDetails(DynamicDocument):
     firstname=StringField()
     lastname=StringField()
     mobile = StringField()
     altmobile = StringField()
     email=StringField()     
     rewardpoints=StringField()
     discount = StringField()
     createddate = StringField()
     createdat=StringField()
     purchase_value=FloatField(default=0)
     password = StringField()
     gst_number=StringField()
     coupon_info=ListField(EmbeddedDocumentField(CustomerCoupon))
     otp=StringField()
     status=StringField()
     billing_address=ListField(EmbeddedDocumentField(BillingShippingAddress))
     shipping_address=ListField(EmbeddedDocumentField(BillingShippingAddress))
     
class Reviews(DynamicDocument):
     prod_desc=StringField()
     rating=StringField()
     rating_comments = StringField()
     
class FooterUrlLink(EmbeddedDocument):
     footerimageurl=StringField()
     footerimagelink=StringField()

class Footer(DynamicDocument):
     footername=StringField()
     imageurllink=ListField(EmbeddedDocumentField(FooterUrlLink))

class Header(DynamicDocument):
     headername=StringField()
     headercontactno=StringField()
     headerlogo = StringField()
     
class WishList(DynamicDocument):
     user_id=StringField()
     product_name = ListField()
          
class Contact_Us(DynamicDocument):
     to=StringField()
     from_=StringField()
     message=StringField()
     subject=StringField()


class Sms_Config(EmbeddedDocument):
     url=StringField()
     username=StringField()
     password=StringField()

     
class Email_Config(EmbeddedDocument):
     url=StringField()
     auth=StringField()

     
class Configuration(DynamicDocument):
     deafault_country_code=StringField()
     admin_mail=ListField()
     admin_mobile=ListField()
     sms=ListField(EmbeddedDocumentField(Sms_Config))
     email=ListField(EmbeddedDocumentField(Email_Config))

class Reviews_info(DynamicDocument):
     prod_desc=StringField()
     rating=StringField()
     email=StringField()
     mobile_number=StringField()
     review =StringField()
     rating_comments = StringField()
     user = StringField()
     mobile=StringField()
     created_date = DateTimeField( "created_date",format="%d/%m/%y",default=datetime.datetime.now)
     status=StringField(default='Created')

class Notify_info(DynamicDocument):
     email = StringField()
     mobile_number=StringField()
     productname=StringField()
     current_date = DateTimeField( "created_date",format="%d/%m/%y",default=datetime.datetime.now)
     
class RandomCoupons(DynamicDocument):
     cu_number = StringField()

     
class ReferFriend(DynamicDocument):
     prod_name = StringField()
     email=StringField()
     refer_email=StringField()


class BannerUrlLink(EmbeddedDocument):
     bannerimageurl=StringField()
     bannerimagelink=StringField()

class Banner(DynamicDocument):
     bannername=StringField()
     imageurllink=ListField(EmbeddedDocumentField(BannerUrlLink))

	 
class Collections(DynamicDocument):
     name=StringField()
     imageurl=StringField()
     imagelink = StringField()

	 
class Brand(DynamicDocument):
     brandname=StringField()
     brandurl=StringField()
     brandlink = StringField()
     brandfooterurl=StringField()
     brandtype=StringField()
	 
class OrderCoupons(DynamicDocument):
     user_id=StringField()
     coupon_name=StringField()
     coupon_code=StringField()
     discount=StringField()
     typeflat=StringField()
     maxvalue=StringField()
     from_date=StringField()
     end_date=StringField()
     min_order_value=StringField()
     created_date=StringField()
     createdBy=StringField()
     terms_conditions=StringField()
     imageurl=StringField()
     status=StringField(default='Inactive')
     maxvalue=StringField()

class CompareProducts(DynamicDocument):
     user_id=StringField()
     product_name = ListField()
class test(DynamicDocument):
     empid=StringField()
     name = StringField()
     email = StringField()
     mobile = StringField()
     qalification = StringField()

class reg(DynamicDocument):
     fname=StringField()
     lname = StringField()
     email = StringField()
     mobile = StringField()
     address = StringField()
     password = StringField()
     cnfrmPwd = StringField()

class addtocart(DynamicDocument):
     username=StringField()
     category = StringField()
     subcategory = StringField()
     modelno = StringField()
     image=StringField()
     upload_mrp = StringField()
     upload_discount = StringField()
     upload_netPrice = StringField()     

     
     
     

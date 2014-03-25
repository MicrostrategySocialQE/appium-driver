'''
Created on Aug 6, 2013

@author: Zhenyu

This uimap is for Trela 3.6
'''


class tag_names:
    
    label = "UIAStaticText"
    image = "UIAImage"

    
class login:
    connect_with_facebook = "Connect with Facebook"
    sign_up_with_email = "Sign up with Email"
    sign_in = "Sign In"
    proceed_as_guest = "Proceed as Guest"
    
    
class facebook:
    
    email = "email"
    password = "pass"
    login = "login"
    OK = "__CONFIRM__"
    close = "close"
    
    
class signup:
    first_name = "//window[1]/scrollview[1]/textfield[1]"
    last_name = "//window[1]/scrollview[1]/textfield[2]"
    email = "//window[1]/scrollview[1]/textfield[3]" 
    password = "//window[1]/scrollview[1]/secure[1]"
    gender = ["mobile: tap", {"tapCount": 1, "touchCount": 1, "duration": 0.5, "x": 50, "y": 325 }]
    date_of_birth = "//window[1]/scrollview[1]/textfield[5]"
    
    submit = "Submit"
    
    
class signin:
    email = "email address"
    password = "password"
    submit = "Sign in"
    
    
class general:
    sider_bar = {"ios": "icon inbox list",
                 "android": "home_button"
    }
    inbox = "Inbox" 
    vouchers = "Vouchers"
    receipts = "Receipts"
    my_guess_id = "My GUESS ID"
    gift_cards = "Gift Cards"
    shop = "Shop"
    store_locator = "Store Locator"
    socialize = "Socialize"
    sign_in = "Sign In"
    done = "Done"
    explore_and_earn = "Explore and Earn"
    explore = "Explore"
    shop = "Shop"
    store_locator = "Store Locator"
    saved_offers = "Saved Offers"
    
    max_window = "//window[1]"
    geofence_close = "icon x"
    back_button = "icon arrow back"
    
class account:
    link_your_facebook_account = "Link Your Facebook Account"
    edit_profile = "Edit Profile"
    archive = "//window[1]/tableview[1]/cell[3]/text[1]"
    recycle_bin = "//window[1]/tableview[1]/cell[4]/text[1]"
    invite_your_friends = "Invite Your Friends"
    contact_us = "Contact Us"
    privacy_policy = "Privacy Policy"
    terms_of_use = "Terms of Use"
    signout = "Sign Out"
    signoutok = "//window[3]/actionsheet[1]/button[1]"

    
    
class offer:
    back = "icon arrow back"
    action = "action icon"
    facebook = "//window[1]/image[1]/UIACollectionView[1]/UIACollectionCell[1]/text[1]"
    email = "//window[1]/image[1]/UIACollectionView[1]/UIACollectionCell[2]/text[1]"
    cancel = "Cancel"
    send = "Send"
    delete_draft = "//window[1]/actionsheet[1]/button[1]"
    claim_now = "Claim Now"
    gift = "//window[1]/image[1]/UIACollectionView[1]/UIACollectionCell[6]/text[1]"
    gift_icon = "icon gift on button"
    
    search_box = "//window[1]/tableview[1]/searchbar[1]"
    coupon_code = "//window[1]/scrollview[1]/scrollview[2]"
    get_new = "button refresh"
    
    accept_gift = "Accept Gift"
    
    search_from_facebook = "//window[1]/tableview[1]/cell[1]/text[1]"

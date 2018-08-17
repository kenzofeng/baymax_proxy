*** Settings ***
Library           Doraemon
Resource          inner.robot

*** Test Cases ***
TC01.001
    bookingHold    http://172.27.0.63:80/expedia-endpoint/soap-ec2/    httpProviderRQ_filters=['.//*[@RequestId]']    httpProviderRQ_namesp=None    httpChannelRS_filters=['.//x:OTA_HotelResRS[@TimeStamp]','.//x:UniqueID[@ID]']    httpChannelRS_namesp={'x':'http://www.opentravel.org/OTA/2003/05'}

TC01.002
    bookingCommit    http://172.27.0.63:80/expedia-endpoint/soap-ec2/    httpProviderRQ_filters=['.//*[@RequestId]']    httpProviderRQ_namesp=None    httpChannelRS_filters=['.//x:OTA_HotelResRS[@TimeStamp]','.//x:UniqueID[@ID]']    httpChannelRS_namesp={'x':'http://www.opentravel.org/OTA/2003/05'}

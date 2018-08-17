*** Settings ***
Suite Setup       start
Library           Doraemon

*** Keywords ***
start
    Stop Server    9011    8011
    Comment    DB Execute Sql    ./Expedia-BW-Booking/BWDataClear.sql    host=172.27.0.184
    Comment    DB Execute Sql    ./Expedia-BW-Booking/EXPDataClear.sql    host=172.27.0.63
    ClearHilton
    clearEXP

ClearHilton
    DB Execute Sql String    USE hilton_adapter;DELETE FROM modify_additional_data;DELETE FROM notify_task;DELETE FROM reservation_item;DELETE FROM reservation;    host=172.27.0.168

ClearEXP
    DB Execute Sql String    USE expedia_endpoint;DELETE FROM reservation;DELETE FROM notify_task;DELETE FROM callback_task;    host=172.27.0.63

*** Settings ***
Suite Setup       start
Library           Doraemon

*** Keywords ***
start
    Stop Server    9011    8011
    Comment    DB Execute Sql    ./Expedia-BW-Booking/BWDataClear.sql    host=172.27.0.184
    Comment    DB Execute Sql    ./Expedia-BW-Booking/EXPDataClear.sql    host=172.27.0.63
    clearBW
    clearEXP

ClearBW
    DB Execute Sql String    USE bestwestern_adapter;DELETE FROM reservation_room_stay;DELETE FROM reservation_entity;DELETE FROM reservation_event;    host=172.27.0.184

ClearEXP
    DB Execute Sql String    USE expedia_endpoint;DELETE FROM reservation;DELETE FROM notify_task;DELETE FROM callback_task;    host=172.27.0.63

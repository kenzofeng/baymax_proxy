*** Settings ***
Library           Doraemon

*** Keywords ***
booking
    [Arguments]    ${Http_URL}    ${Http_Port_Provider}=8011    ${Http_Port_Channel}=9011    ${httpChannelRQ_filters}=None    ${httpChannelRQ_namesp}=None    ${httpProviderRQ_filters}=None
    ...    ${httpProviderRQ_namesp}=None
    @{HttpRQ}=    Test HTTP Client Requests
    Comment    @{HttpProviderRS}=    Test HTTP Server Responses
    Comment    @{HttpChannelRS}=    Test HTTP Server Responses
    @{HttpProviderRS}=    Test Data    HttpRS.*-BW.*.xml
    @{HttpChannelRS}=    Test Data    HttpRS.*-EXP.*.xml
    Run Http Server    ${Http_Port_Provider}    200    @{HttpProviderRS}
    Run Http Server    ${Http_Port_Channel}    200    @{HttpChannelRS}
    Run Http Client    ${Http_URL}    POST    @{HttpRQ}[0]
    @{httpRSActual}=    Get Http Client Responses
    ${httpProviderRQActual}=    Get Http Server Request    ${Http_Port_Provider}
    ${httpChannelRQActual}=    Get Http Server Request    ${Http_Port_Channel}
    Comment    ${expected_HttpProviderRQ}=    Test HTTP Server Expected Requests
    Comment    ${expected_HttpChannelRQ}=    Test HTTP Server Expected Requests
    ${expected_HttpProviderRQ}=    Test Data    expected-HttpRQ.*-BW.*.xml
    ${expected_HttpChannelRQ}=    Test Data    expected-HttpRQ.*-EXP.*.xml
    Comment    @{expected_httpRS}=    Test HTTP Client Expected Responses
    Comment    Xml Compare    @{httpRSActual}[0]    @{expected_httpRS}[0]
    : FOR    ${request}    ${expected_request}    IN ZIP    ${httpProviderRQActual}    ${expected_HttpProviderRQ}
    \    Xml Compare    ${request}    ${expected_request}    tagfilters=${httpProviderRQ_filters}    namespaces=${httpProviderRQ_namesp}
    :FOR    ${request}    ${expected_request}    IN ZIP    ${httpChannelRQActual}    ${expected_HttpChannelRQ}
    \    Xml Compare    ${request}    ${expected_request}    tagfilters=${httpChannelRQ_filters}    namespaces=${httpChannelRQ_namesp}
    Should Not Be Empty    ${httpProviderRQActual}
    Should Not Be Empty    ${httpProviderRQActual}

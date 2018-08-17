*** Settings ***
Library           Doraemon

*** Keywords ***
bookingHold
    [Arguments]    ${Http_URL}    ${Http_Port_Provider}=6011    ${Http_Port_Channel}=9011    ${httpChannelRS_filters}=None    ${httpChannelRS_namesp}=None    ${httpProviderRQ_filters}=None
    ...    ${httpProviderRQ_namesp}=None
    @{HttpRQ}=    Test HTTP Client Requests
    @{HttpProviderRS}=    Test Data    HttpRS.*-HI.*.xml
    Run Http Server    ${Http_Port_Provider}    200    @{HttpProviderRS}
    Comment    Run Http Server    ${Http_Port_Channel}    200    @{HttpChannelRS}
    Run Http Client    ${Http_URL}    POST    @{HttpRQ}[0]
    @{httpRSActual}=    Get Http Client Responses
    ${httpProviderRQActual}=    Get Http Server Request    ${Http_Port_Provider}
    Comment    ${httpChannelRQActual}=    Get Http Server Request    ${Http_Port_Channel}
    Comment    ${expected_HttpProviderRQ}=    Test HTTP Server Expected Requests
    Comment    ${expected_HttpChannelRQ}=    Test HTTP Server Expected Requests
    ${expected_HttpProviderRQ}=    Test Data    expected-HttpRQ.*-HI.*.xml
    Comment    ${expected_HttpChannelRQ}=    Test Data    expected-HttpRQ.*-EXP.*.xml
    @{expected_httpRS}=    Test HTTP Client Expected Responses
    Xml Compare    @{httpRSActual}[0]    @{expected_httpRS}[0]    tagfilters=${httpChannelRS_filters}    namespaces=${httpChannelRS_namesp}
    : FOR    ${request}    ${expected_request}    IN ZIP    ${httpProviderRQActual}    ${expected_HttpProviderRQ}
    \    Xml Compare    ${request}    ${expected_request}    tagfilters=${httpProviderRQ_filters}    namespaces=${httpProviderRQ_namesp}
    Comment    : FOR    ${request}    ${expected_request}    IN ZIP    ${httpChannelRQActual}    ${expected_HttpChannelRQ}
    Comment    \    Xml Compare    ${request}    ${expected_request}    tagfilters=${httpChannelRQ_filters}    namespaces=${httpChannelRQ_namesp}
    Should Not Be Empty    ${httpProviderRQActual}
    Should Not Be Empty    ${httpProviderRQActual}

bookingCommit
    [Arguments]    ${Http_URL}    ${Http_Port_Provider}=6011    ${Http_Port_Channel}=9011    ${httpChannelRS_filters}=None    ${httpChannelRS_namesp}=None    ${httpProviderRQ_filters}=None
    ...    ${httpProviderRQ_namesp}=None
    @{HttpRQ}=    Test HTTP Client Requests
    Comment    @{HttpProviderRS}=    Test HTTP Server Responses
    Comment    @{HttpChannelRS}=    Test HTTP Server Responses
    @{HttpProviderRS}=    Test Data    HttpRS.*-HI.*.json
    ${url_HttpRS1}    Set Reponse    @{HttpProviderRS}[0]    {}
    ${url_HttpRS2}    Set Reponse    @{HttpProviderRS}[1]    {"Content-Type":"text/html; charset=utf-8", "Location":"/reservations/HTL01001"}
    Comment    @{HttpChannelRS}=    Test Data    HttpRS.*-EXP.*.xml
    Run Http Server    ${Http_Port_Provider}    200    ${url_HttpRS1}    ${url_HttpRS2}
    Comment    Run Http Server    ${Http_Port_Channel}    200    @{HttpChannelRS}
    Run Http Client    ${Http_URL}    POST    @{HttpRQ}[0]
    @{httpRSActual}=    Get Http Client Responses
    Comment    log    @{httpRSActual}
    ${httpProviderRQActual}=    Get Http Server Request    ${Http_Port_Provider}
    Comment    ${httpChannelRQActual}=    Get Http Server Request    ${Http_Port_Channel}
    Comment    ${expected_HttpProviderRQ}=    Test HTTP Server Expected Requests
    Comment    ${expected_HttpChannelRQ}=    Test HTTP Server Expected Requests
    ${expected_HttpProviderRQ}=    Test Data    expected-HttpRQ.*-HI.*.json
    Comment    ${expected_HttpChannelRQ}=    Test Data    expected-HttpRQ.*-EXP.*.xml
    @{expected_httpRS}=    Test HTTP Client Expected Responses
    Xml Compare    @{httpRSActual}[0]    @{expected_httpRS}[0]    tagfilters=${httpChannelRS_filters}    namespaces=${httpChannelRS_namesp}
    :FOR    ${request}    ${expected_request}    IN ZIP    ${httpProviderRQActual}    ${expected_HttpProviderRQ}
    \    Json Compare    ${request}    ${expected_request}
    Comment    : FOR    ${request}    ${expected_request}    IN ZIP    ${httpChannelRQActual}    ${expected_HttpChannelRQ}
    Comment    \    Xml Compare    ${request}    ${expected_request}    tagfilters=${httpChannelRQ_filters}    namespaces=${httpChannelRQ_namesp}
    Should Not Be Empty    ${httpProviderRQActual}
    Should Not Be Empty    ${httpProviderRQActual}

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 15:48:15 2024

@author: oozi
"""

# %% import
import requests
import xml.etree.ElementTree as ET
import datetime as dt
import numpy as np
import tkinter as tk
from tkinter import ttk




  


# %% define URLs and headers


with open(".api_token.txt", "r") as token_file :
    api_token = token_file.readline()

url = 'https://api.opentransportdata.swiss/ojp2020'


headers = {'Content-Type': 'application/xml',
           'Authorization': 'Bearer ' + api_token
           }


# %% train station request

def trainstation_request() :
    
    now = dt.datetime.now() + dt.timedelta(minutes=1)
    
    now = now.strftime('%Y-%m-%d'+'T'+'%H:%M:%S'+'Z')
    
    with open(".didok_trainstation.txt", "r") as didok_file :
        didok = didok_file.readline()
        
    
    xml_request = '''<?xml version="1.0" encoding="UTF-8"?>
    <OJP xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://www.siri.org.uk/siri" version="1.0" xmlns:ojp="http://www.vdv.de/ojp" xsi:schemaLocation="http://www.siri.org.uk/siri ../ojp-xsd-v1.0/OJP.xsd">
        <OJPRequest>
            <ServiceRequest>
                <RequestTimestamp>'''+now+'''</RequestTimestamp>
                <RequestorRef>API-Explorer_test</RequestorRef>
                <ojp:OJPStopEventRequest>
                    <RequestTimestamp>'''+now+'''</RequestTimestamp>
                    <ojp:Location>
                        <ojp:PlaceRef>
                            <StopPlaceRef>'''+didok+'''</StopPlaceRef>
                            <ojp:LocationName>
                                <ojp:Text>-</ojp:Text>
                            </ojp:LocationName>
                        </ojp:PlaceRef>
                        <ojp:DepArrTime>'''+now+'''</ojp:DepArrTime>
                    </ojp:Location>
                    <ojp:Params>
                        <ojp:NumberOfResults>10</ojp:NumberOfResults>
                        <ojp:StopEventType>departure</ojp:StopEventType>
                        <ojp:IncludePreviousCalls>false</ojp:IncludePreviousCalls>
                        <ojp:IncludeOnwardCalls>false</ojp:IncludeOnwardCalls>
                        <ojp:IncludeRealtimeData>true</ojp:IncludeRealtimeData>
                    </ojp:Params>
                </ojp:OJPStopEventRequest>
            </ServiceRequest>
        </OJPRequest>
    </OJP>'''
    
    return xml_request


# %% bus stop request

def busstop_request() :
    
    now = dt.datetime.now() + dt.timedelta(minutes=2)
    
    now = now.strftime('%Y-%m-%d'+'T'+'%H:%M:%S'+'Z')

    with open(".didok_busstop.txt", "r") as didok_file :
        didok = didok_file.readline()

    xml_request = '''<?xml version="1.0" encoding="UTF-8"?>
    <OJP xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://www.siri.org.uk/siri" version="1.0" xmlns:ojp="http://www.vdv.de/ojp" xsi:schemaLocation="http://www.siri.org.uk/siri ../ojp-xsd-v1.0/OJP.xsd">
        <OJPRequest>
            <ServiceRequest>
                <RequestTimestamp>'''+now+'''</RequestTimestamp>
                <RequestorRef>API-Explorer_test</RequestorRef>
                <ojp:OJPStopEventRequest>
                    <RequestTimestamp>'''+now+'''</RequestTimestamp>
                    <ojp:Location>
                        <ojp:PlaceRef>
                            <StopPlaceRef>'''+didok+'''</StopPlaceRef>
                            <ojp:LocationName>
                                <ojp:Text>-</ojp:Text>
                            </ojp:LocationName>
                        </ojp:PlaceRef>
                        <ojp:DepArrTime>'''+now+'''</ojp:DepArrTime>
                    </ojp:Location>
                    <ojp:Params>
                        <ojp:NumberOfResults>15</ojp:NumberOfResults>
                        <ojp:StopEventType>departure</ojp:StopEventType>
                        <ojp:IncludePreviousCalls>false</ojp:IncludePreviousCalls>
                        <ojp:IncludeOnwardCalls>false</ojp:IncludeOnwardCalls>
                        <ojp:IncludeRealtimeData>true</ojp:IncludeRealtimeData>
                    </ojp:Params>
                </ojp:OJPStopEventRequest>
            </ServiceRequest>
        </OJPRequest>
    </OJP>'''

    return xml_request


# %% request trains

def request_trains(xml_request):
    
    xml_string = requests.post(url, data = xml_request, headers = headers).text
    
    retrieved_train_data = ET.fromstring(xml_string)
    
    
    trains = np.array([["img/sbb_logo.png", "Ligne", "Destination", "Voie", "Retard"]])

    
    # Define the namespaces
    namespaces = {
        'siri': 'http://www.siri.org.uk/siri',
        'ojp': 'http://www.vdv.de/ojp'
    }
    
    # Extract and print some information from the XML
    stop_event_results = retrieved_train_data.findall('.//ojp:StopEventResult', namespaces)
    
    for result in stop_event_results:
        
        timetabled_time = result.find('.//ojp:ServiceDeparture/ojp:TimetabledTime', namespaces).text
        
        estimated_time = result.find('.//ojp:ServiceDeparture/ojp:EstimatedTime', namespaces)
        estimated_time = estimated_time.text if estimated_time is not None else 'N/A'
        
        published_line_name = result.find('.//ojp:PublishedLineName/ojp:Text', namespaces).text
        
        destination_text = result.find('.//ojp:DestinationText/ojp:Text', namespaces).text
        
        destination_text = destination_text.encode('latin1').decode('utf-8')
        
        track = result.find('.//ojp:PlannedQuay/ojp:Text', namespaces)
        track = track.text if track is not None else '-'
        
        
        timetabled_time = dt.datetime.strptime(timetabled_time, '%Y-%m-%d'+'T'+'%H:%M:%S'+'Z')
        
        
        if estimated_time != 'N/A' :
            estimated_time = dt.datetime.strptime(estimated_time, '%Y-%m-%d'+'T'+'%H:%M:%S'+'Z')
            
            if estimated_time != timetabled_time :
                delay = estimated_time - timetabled_time
                delay = delay.total_seconds() / 60
                #delay = delay.strftime("%M")
            else:
                delay = ""
            
        else:
            delay = ""
        
        
        timetabled_time = timetabled_time.strftime("%H:%M")
        
        
        trains = np.concatenate((trains, [[timetabled_time, published_line_name, destination_text, track, delay]]), axis = 0)    
        
        
    return trains


# %% request buses


def request_buses(xml_request):
    
    xml_string = requests.post(url, data = xml_request, headers = headers).text
    
    retrieved_buses_data = ET.fromstring(xml_string)
    
    buses = np.array([["Ligne", "Direction", "Départ"]])

    
    # Define the namespaces
    namespaces = {
        'siri': 'http://www.siri.org.uk/siri',
        'ojp': 'http://www.vdv.de/ojp'
    }
    
    
    # Extract and print some information from the XML
    stop_event_results = retrieved_buses_data.findall('.//ojp:StopEventResult', namespaces)
    
    
    for result in stop_event_results:
        
        timetabled_time = result.find('.//ojp:ServiceDeparture/ojp:TimetabledTime', namespaces).text
        
        estimated_time = result.find('.//ojp:ServiceDeparture/ojp:EstimatedTime', namespaces)
        estimated_time = estimated_time.text if estimated_time is not None else 'N/A'
        
        published_line_name = result.find('.//ojp:PublishedLineName/ojp:Text', namespaces).text
        

        
        destination_text = result.find('.//ojp:DestinationText/ojp:Text', namespaces).text
        
        destination_text = destination_text.encode('latin1').decode('utf-8')
        
        track = result.find('.//ojp:PlannedQuay/ojp:Text', namespaces)
        track = track.text if track is not None else '-'
        

        
        if estimated_time != 'N/A' :
            estimated_time = dt.datetime.strptime(estimated_time, '%Y-%m-%d'+'T'+'%H:%M:%S'+'Z')
            
            awaiting_time = estimated_time - dt.datetime.now()
            
            awaiting_time = awaiting_time.total_seconds() // 60
            
        else:
            timetabled_time = dt.datetime.strptime(timetabled_time, '%Y-%m-%d'+'T'+'%H:%M:%S'+'Z')
            
            awaiting_time = timetabled_time - dt.datetime.now()
            
            awaiting_time = awaiting_time.total_seconds() // 60
        
        
        awaiting_time = str(f"{int(awaiting_time)}'")
        
        buses = np.concatenate((buses, [[published_line_name, destination_text, awaiting_time]]), axis = 0)    
        
        
    return buses



# %% check functions
if __name__ == '__main__':
    trains = request_trains(trainstation_request())
    buses = request_buses(busstop_request())

    


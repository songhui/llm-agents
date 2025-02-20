CREATE (an:ANALYTICS {name: "LUMEN_analytics"});

CREATE (n:ASSET {name:"CSMS", uc: 1,  layer:"Functional", description: "Charging Station Management System: cloud-based platform for electric vehicle charging station management.",  ip: "192.168.21.70"});
CREATE (n:ASSET {name:"switch_1",  uc: 1, layer:"Network", description: "Switch.",  ip: "192.168.21.215"});
CREATE (n:ASSET {name:"switch_2",  uc: 1, layer:"Network", description: "Switch.",  ip: "192.168.21.128"});
CREATE (n:ASSET {name:"router",  uc: 1, layer:"Network", description: "Router that provides Internet access and functions as a VPN gateway and firewall.",  ip: "192.168.21.120"});
CREATE (n:ASSET {name:"EVCS_1",  uc: 1, layer:"Physical", description: "Electric Vehicle Charging Station.",  ip: "192.168.21.233"});
CREATE (n:ASSET {name:"EVCS_2",  uc: 1, layer:"Physical", description: "Electric Vehicle Charging Station.",  ip: "192.168.21.225"});
CREATE (n:ASSET {name:"FPR",  uc: 1, layer:"Physical", description: "Safeguards against grid anomalies such as overcurrent or overvoltage events.",  ip: "192.168.21.228"});

MATCH (a:ASSET), (b:ASSET) WHERE a.name = "EVCS_1" AND b.name = "FPR"
CREATE (b)-[r:DistributesTo]->(a);

MATCH (a:ASSET), (b:ASSET) WHERE a.name = "EVCS_2" AND b.name = "FPR"
CREATE (b)-[r:DistributesTo]->(a);

MATCH (a:ASSET), (b:ASSET), (c:ASSET) WHERE a.name = "EVCS_1" AND b.name = "EVCS_2" AND c.name = "switch_1"
CREATE (a)-[r:ConnectTo]->(c)<-[j:ConnectTo]-(b);

MATCH (a:ASSET), (b:ASSET), (c:ASSET) WHERE a.name = "switch_2" AND b.name = "switch_1" AND c.name = "router"
CREATE (b)-[r:ConnectTo]->(c)-[j:ConnectTo]->(a);

MATCH (a:ASSET), (b:ASSET) WHERE a.name = "switch_2" AND b.name = "CSMS"
CREATE (b)-[r:ConnectTo]->(a);

CREATE (n:DATASOURCE {name:"CSMS_CIC", uc: 1, type:"cicflowmeter", format:"timeseries", endpoint:"UC1.cicflowmeter.flows"});
CREATE (n:DATASOURCE {name:"CSMS_OCPP", uc: 1, type:"ocppflowmeter", format:"timeseries", endpoint:"UC1.ocppflowmeter.flows"});
CREATE (n:DATASOURCE {name:"CSMS_OCPP_logs", uc: 1, type:"ocpplogs", format:"timeseries", endpoint:"UC1.ocpploggenerator.logs"});
CREATE (n:DATASOURCE {name:"CSMS_MetricBeat", uc: 1, type:"metricbeat", format:"timeseries", endpoint:"UC1.csms.metricbeat"});

MATCH (a:DATASOURCE), (b:ASSET) WHERE a.name = "CSMS_CIC" AND b.name = "switch_2"
CREATE (a)-[r:DataSourceOf]->(b);
MATCH (a:DATASOURCE), (b:ASSET) WHERE a.name = "CSMS_OCPP" AND b.name = "switch_2"
CREATE (a)-[r:DataSourceOf]->(b);
MATCH (a:DATASOURCE), (b:ASSET) WHERE a.name = "CSMS_OCPP_logs" AND b.name = "switch_2"
CREATE (a)-[r:DataSourceOf]->(b);
MATCH (a:DATASOURCE), (b:ASSET) WHERE a.name = "CSMS_MetricBeat" AND b.name = "CSMS"
CREATE (a)-[r:DataSourceOf]->(b);

MATCH (a:ASSET) WHERE a.name = "switch_1" CREATE (s:STATICDATA {name: a.name + "_StaticData", uc: 1, type: "", file_name: "", add_date: "", format: ""})
MERGE (s)-[:DataOf]->(a);
MATCH (a:ASSET) WHERE a.name = "switch_2" CREATE (s:STATICDATA {name: a.name + "_StaticData", uc: 1, type: "", file_name: "", add_date: "", format: ""})
MERGE (s)-[:DataOf]->(a);

MATCH (n) SET n.uid = apoc.create.uuid();

MATCH (a:ASSET)<-[:DataSourceOf]-(d:DATASOURCE)
SET d.bucket = d.uid;

MATCH (a:ASSET)<-[:DataOf]-(d:STATICDATA)
SET d.bucket = d.uid;


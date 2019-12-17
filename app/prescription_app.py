import dash
import pickle
import plotly.express as px
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

with open('../app/static_data.pckl', 'rb') as inf:
    data = pickle.load(inf)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#diagnosis = ['Acute Cystitis Females >12 years old,Uncomplicated', 'Pneumonia- Adult: Community acquired, mild to moderate, Outpatient without comorbidity/modifying factors']
diagnosis_treatments = {'Acute Cystitis Females >12 years old,Uncomplicated': ['1st level - TMP/SMX 1 DS tab po bid  for 3 days', '1st level - Trimethoprim 200mg once po daily for 3 days', '1st level - Macrobid 100 mg po bid for 5 days', '2nd level - Amoxicillin 500mg po TID for 7 days', '2nd level - Norfloxacin 400mg po bid for 3 days', '2nd level - Ciprofloxacin 250mg po bid for 3 days', '3rd level - Cephalexin 500mg po bid for 7 days', '3rd level - Levoquin 250mg po daily for 3 days'],
                        'Pneumonia- Adult: Community acquired, mild to moderate, Outpatient without comorbidity/modifying factors': ['1st level - Amoxicillin 1g po tid for 7 days', '2nd level - Doxycycline 100mg po bid day 1 and then qd days 2-7', '2nd level - Azithromycin 250mg 2 tabs day 1 and then one tab days 2-5', '2nd level - Clarithromycin 500mg po once daily for 7 days', '3rd level - Levofloxacin 750mg po qd for 5 days', '3rd level - Moxifloxacin 400mg po once daily for 5 days']

                       }
def pres_behavior_chart(bars):
    fig = px.bar(
        bars,
        x="variable",
        y="value",
        color="class",
        barmode="group",
    )
    fig.layout.xaxis.title = "Prescriptions for female patients between 20-30 years for the same diagnosis"
    fig.layout.yaxis.title = "Percentage of prescriptions for the given class"
    return fig



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Mission Prescription'


left_text = '''
## Mission Prescription
### Supporting clinicians with locally optimised antibiotic prescription options
90% of antibiotics are prescribed in primary care, using systems that push 100% of the mental load on the clinician.
We propose to use **existing** AMR data to automatically select+suggest the **locally** most effective 1st line antibiotic based on a diagnosis.
To nudge clinicians toward accepting the suggestion, our module shows them how often they prescribe 2nd and 3rd line antibiotics in relation to their peers.
The module will therefore simultaneously increase the prescription of effective 1st line antibiotics, as well as decrease the number of 2nd and 3rd line antibiotics that are prescribed overall.
'''

right_text = '''
## The project
Mission prescription won [1st prize](https://www.jpiamr.eu/team-mission-prescription-is-the-winner-of-hacking-amr-2019) at the #HackingAMR2019 event of JPIAMR in Stockholm,
the (improved) slides of the pitch can be found [here](https://speakerdeck.com/davhin/jpiamr-hacking-amr-2019-team-mission-prescription).
The team members are Sabrina Wong ([@sabrinawong88](https://twitter.com/sabrinawong88)), David Barber, Sumeet Tiwari ([@sumeet_kumart07](https://twitter.com/sumeet_kumart07), Robert Koch Institute), Lennard Epping ([@LennardEpp](https://twitter.com/LennardEpp), Robert Koch Institute), Vendela Wiener, Ewan Gray, and David Hinrichs ([@davhin11](https://twitter.com/davhin11), idalab)
'''

app.layout = html.Div(children=[
        html.Div([
            html.Div([
            dcc.Markdown(left_text),
            ],
                className='six columns'),
            html.Div([
            dcc.Markdown(right_text),
            ],
                className='six columns')
                ],
            className='row'),
    html.Div([
        html.Div([
            html.Hr(),
            html.Hr(),
            html.H4("Your diagnosis"),
            dcc.RadioItems(
                id='diagnosis-options',
                options=[{'label': i, 'value': i} for i in list(diagnosis_treatments.keys())],
                value=list(diagnosis_treatments.keys())[0],
                labelStyle={'display': 'inline-block'}
            )])],
        className='row')
    ,
    html.Div([
        html.Div([
            html.H4("Your prescription behavior for 2nd and 3rd line antibiotics"),
            dcc.Graph(id='prescribing-graph')
        ],
            className='six columns'),
        html.Div([
            html.H4("Your treatment options"),
            html.Label(['Recommended antibiotics for your area',
            dcc.Dropdown(id='dropdown-treatments'
                        )]),
            html.Hr(),
            html.Button(id='submit-button', n_clicks=0, children='Generate prescription'),
            html.Div(id='output-prescription', children=""),
            html.Hr(),
            html.Button(id='submit-button-final', n_clicks=0, children='SEND prescription'),
            html.Div(id='output-prescription-final', children="")
        ],
            className='six columns')
    ],
        className='row')
])


@app.callback(Output('output-prescription', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('dropdown-treatments', 'value')])
def send_prescription(n_clicks, prescription):
    if n_clicks > 0:
        return "Prescription of {} for patient {}".format(prescription.split('- ')[1], "Christina Miller, female, 25 years")


@app.callback(Output('output-prescription-final', 'children'),
              [Input('submit-button-final', 'n_clicks')],
              [State('output-prescription', 'children')])
def send_prescription_final(n_clicks, prescription):
    if n_clicks > 0:
        return "Sent prescription to pharmacy"


@app.callback(
    Output('dropdown-treatments', 'options'),
    [Input('diagnosis-options', 'value')])
def set_dropdown_treatments_1st(selected_diagnosis):

    return [{'label': i, 'value': i} for i in diagnosis_treatments[selected_diagnosis]]


@app.callback(
    Output('dropdown-treatments', 'value'),
    [Input('diagnosis-options', 'value')])
def set_dropdown_treatments(selected_diagnosis):
    return diagnosis_treatments[selected_diagnosis][0]


@app.callback(
    Output('prescribing-graph', 'figure'),
    [Input('diagnosis-options', 'value')])
def plot_prescribing_behavior(diagnosis):
    return pres_behavior_chart(data[diagnosis])




if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8060)

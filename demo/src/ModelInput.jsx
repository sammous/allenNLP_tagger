import React from 'react';
import Button from './components/Button'
import ModelIntro from './components/ModelIntro'


// TODO: These are some quickly-accessible examples to try out with your model.  They will get
// added to the select box on the demo page, and will auto-populate your input fields when they
// are selected.  The names here need to match what's read in `handleListChange` below.

const examples = [
  {
    long_text_input:
    // eslint-disable-next-line
      "Fiscal Policy and the Labor Market in the Euro Area : Multiplier, Spillover effects and Fiscal Federalism​\
This thesis aims at contributing to the recent studies which investigate the short-run effects of fiscal policy \
on economic activity. More precisely, three main aspects of fiscal policy in the short run are analyzed. First, one major message is that the impact of \
fiscal policy on the economy depends strongly on the fiscal instrument used by the government. \
Rising transfers to households, increasing public investment or cutting social protection tax trigger very different effects on key macroeconomic variables and\
especially on output. Second, one large part of this thesis is dedicated to the analysis of the effects of fiscal policy shocks on the labor market. One main \
result is that we cannot determine unemployment fiscal multipliers according to the value of the output\
fiscal multiplier, especially because of the response of the labor force participation to fiscal policy shocks. Third, this is well-known that\
 many elements influence the size of the output fiscal multiplier. Two of these elements are considered throughout this\
thesis: the position of the economy over the business cycle and the behavior of the monetary policy. The two first chapters of this thesis analyze these different aspects in some closed economy models. \
The two last chapters extend this study at the case of a monetary union by investigating the spillover effects of fiscal policy between member states but also the stabilizing properties of fiscal\
transfer mechanisms between member states in order to soften cyclical shocks.​"
  }
];

// TODO: This determines what text shows up in the select box for each example.  The input to
// this function will be one of the items from the `examples` list above.
function summarizeExample(example) {
  return example.long_text_input.substring(0, 60);
}

// TODO: You can give a model name and description that show up in your demo.
const title = "dataESR : Text classifier based on SCOPUS ontology";
const description = (
  <span>
  This demo allows to showcase text classification based on SCOPUS ontology.
  </span>
);

class ModelInput extends React.Component {
  constructor(props) {
    super(props);
    this.handleListChange = this.handleListChange.bind(this);
    this.onClick = this.onClick.bind(this);
  }

  handleListChange(e) {
    if (e.target.value !== "") {
      // TODO: This gets called when the select box gets changed.  You want to set the values of
      // your input boxes with the content in your examples.
      this.long_text_input.value = examples[e.target.value].long_text_input
    }
  }

  onClick() {
    const { runModel } = this.props;

    // TODO: You need to map the values in your input boxes to json values that get sent to your
    // predictor.  The keys in this dictionary need to match what your predictor is expecting to receive.
    runModel({text: this.long_text_input.value});
  }

  render() {

    const { outputState } = this.props;

    return (
      <div className="model__content">
        <ModelIntro title={title} description={description} />
        <div className="form__instructions"><span>Enter text or</span>
          <select disabled={outputState === "working"} onChange={this.handleListChange}>
              <option value="">Choose an example...</option>
              {examples.map((example, index) => {
                return (
                    <option value={index} key={index}>{summarizeExample(example) + "..."}</option>
                );
              })}
          </select>
        </div>

       {/*
         * TODO: This is where you add your input fields.  You shouldn't have to change any of the
         * code in render() above here.  We're giving a couple of example inputs here, one for a
         * larger piece of text, like a paragraph (the `textarea`) and one for a shorter piece of
         * text, like a question (the `input`).  You'll probably want to change the variable names
         * here to match the input variable names in your model.
         */}

        <div className="form__field">
          <label>Document Text</label>
          <textarea ref={(x) => this.long_text_input = x} type="text" autoFocus="true"></textarea>
        </div>

       {/* You also shouldn't have to change anything below here. */}

        <div className="form__field form__field--btn">
          <Button enabled={outputState !== "working"} onClick={this.onClick} />
        </div>
      </div>
    );
  }
}

export default ModelInput;

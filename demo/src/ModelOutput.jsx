import React from 'react';
import HeatMap from './components/heatmap/HeatMap'
import Collapsible from 'react-collapsible'

class ModelOutput extends React.Component {
  render() {

    const { outputs } = this.props;

    // TODO: `outputs` will be the json dictionary returned by your predictor.  You can pull out
    // whatever you want here and visualize it.  We're giving some examples of different return
    // types you might have.  Change names for data types you want, and delete anything you don't
    // need.
    // This is a 1D attention array, which we need to make into a 2D matrix to use with our heat
    // map component.

    var labels = [
      'computational_mathematics', 'oncology', 'chemical_engineering', 'mathematical_physics', 'health_toxicology_and_mutagenesis', 'cultural_studies', 'radiation', 'medical_surgical', 'earth_and_planetary_sciences_miscellaneous', 'general_chemical_engineering', 'cancer_research', 'visual_arts_and_performing_arts', 'statistical_and_nonlinear_physics', 'analytical_chemistry', 'strategy_and_management', 'immunology_and_microbiology', 'speech_and_hearing', 'community_and_home_care',  'infectious_diseases', 'food_science', 'otorhinolaryngology', 'materials_science', 'pathology_and_forensic_medicine', 'computer_graphics_and_computer_aided_design', 'pediatrics_perinatology_and_child_health', 'general_economics_econometrics_and_finance', 'archaeology', 'psychiatry_and_mental_health', 'applied_psychology', 'museology', 'finance', 'pharmacology', 'geology', 'management_science_and_operations_research', 'social_sciences', 'electrical_and_electronic_engineering',  'water_science_and_technology', 'sociology_and_political_science', 'earth_and_planetary_sciences', 'general_physics_and_astronomy', 'pharmacology_medical', 'physics_and_astronomy', 'immunology', 'general_chemistry', 'developmental_and_educational_psychology', 'orthopedics_and_sports_medicine', 'economics_econometrics_and_finance', 'statistics_probability_and_uncertainty', 'biological_psychiatry', 'computer_science_applications', 'biomaterials', 'developmental_biology', 'demography', 'general_social_sciences', 'geriatrics_and_gerontology', 'epidemiology', 'biochemistry_medical', 'mechanics_of_materials', 'algebra_and_number_theory', 'economics_and_econometrics', 'development', 'gerontology', 'ecology', 'biomedical_engineering', 'earth_surface_processes', 'agricultural_and_biological_sciences', 'business_management_and_accounting', 'neurology', 'histology', 'leadership_and_management', 'dermatology', 'surgery', 'health_sciences', 'genetics_clinical', 'pollution', 'medical_laboratory_technology', 'software', 'genetics', 'psychology', 'clinical_psychology', 'astronomy_and_astrophysics', 'behavioral_neuroscience', 'microbiology', 'general_biochemistry_genetics_and_molecular_biology', 'ecology_evolution_behavior_and_systematics', 'parasitology', 'agronomy_and_crop_science', 'organizational_behavior_and_human_resource_management', 'structural_biology', 'medicine', 'management_monitoring_policy_and_law', 'geochemistry_and_petrology', 'urban_studies', 'architecture', 'hardware_and_architecture', 'pharmaceutical_science', 'philosophy', 'physiology_medical', 'space_and_planetary_science', 'agricultural_and_biological_sciences_miscellaneous', 'nature_and_landscape_conservation', 'anthropology', 'plant_science', 'civil_and_structural_engineering', 'environmental_engineering', 'oceanography', 'language_and_linguistics', 'physiology', 'public_health_environmental_and_occupational_health', 'internal_medicine', 'molecular_biology', 'environmental_science', 'pulmonary_and_respiratory_medicine', 'cardiology_and_cardiovascular_medicine', 'cellular_and_molecular_neuroscience', 'arts_and_humanities_miscellaneous', 'animal_science_and_zoology', 'atomic_and_molecular_physics_and_optics', 'transplantation', 'general_agricultural_and_biological_sciences', 'logic', 'toxicology', 'nutrition_and_dietetics', 'endocrinology_diabetes_and_metabolism', 'chiropractics', 'atmospheric_science', 'emergency_medicine', 'religious_studies', 'physical_and_theoretical_chemistry', 'statistics_and_probability', 'general_mathematics', 'horticulture', 'general_earth_and_planetary_sciences', 'health_policy', 'urology', 'issues_ethics_and_legal_aspects', 'ocean_engineering', 'biochemistry_genetics_and_molecular_biology', 'political_science_and_international_relations', 'phychiatric_mental_health', 'human_computer_interaction', 'conservation', 'music', 'mechanical_engineering', 'computer_vision_and_pattern_recognition', 'general_medicine', 'industrial_and_manufacturing_engineering', 'artificial_intelligence', 'radiology_nuclear_medicine_and_imaging', 'applied_microbiology_and_biotechnology', 'social_sciences_miscellaneous', 'general_materials_science', 'social_psychology', 'computational_theory_and_mathematics', 'palaeontology', 'sensory_systems', 'geophysics', 'nuclear_and_high_energy_physics', 'cognitive_neuroscience', 'physical_therapy_sports_therapy_and_rehabilitation', 'soil_science', 'general_environmental_science', 'life_sciences', 'business_and_international_management', 'cell_biology', 'mathematics_miscellaneous', 'general_neuroscience', 'history_and_philosophy_of_science', 'literature_and_literary_theory', 'computational_mechanics', 'applied_mathematics', 'arts_and_humanities', 'bioengineering', 'numerical_analysis', 'fluid_flow_and_transfer_processes', 'history', 'geography_planning_and_development', 'nursing', 'health_social_science', 'condensed_matter_physics', 'endocrinology', 'experimental_and_cognitive_psychology', 'clinical_biochemistry', 'safety_risk_reliability_and_quality', 'engineering', 'medicine_miscellaneous', 'decision_sciences', 'accounting', 'education', 'economics_econometrics_and_finance_miscellaneous', 'health_professions', 'instrumentation', 'general_nursing', 'aquatic_science', 'emergency', 'pharmacology_toxicology_and_pharmaceutics', 'biochemistry', 'clinical_neurology', 'environmental_chemistry', 'forestry', 'linguistics_and_language', 'general_business_management_and_accounting', 'insect_science', 'mathematics', 'control_and_optimization', 'neuropsychology_and_physiological_psychology', 'general_psychology', 'computer_science', 'gastroenterology', 'organic_chemistry', 'radiological_and_ultrasound_technology', 'information_systems_and_management', 'general_arts_and_humanities', 'biophysics', 'anatomy', 'business_management_and_accounting_miscellaneous', 'control_and_systems_engineering', 'neuroscience', 'law', 'theoretical_computer_science', 'classics', 'obstetrics_and_gynaecology', 'physical_sciences', 'metals_and_alloys', 'computer_networks_and_communications', 'ophthalmology', 'analysis', 'environmental_science_miscellaneous', 'public_administration', 'general_engineering', 'general_computer_science', 'physics_and_astronomy_miscellaneous', 'biotechnology', 'chemistry', 'inorganic_chemistry', 'information_systems', 'anesthesiology_and_pain_medicine']

    var xLabelWidth = "auto";

    var dict = labels.map(function(e,i){return[e, outputs['all_predictions'][i]]})
    var sort_dict = dict.sort(function(a, b){return a[1]<b[1]});
    var sorted_labels = sort_dict.map(function(e,i){return e[0]});
    var sorted_predictions = sort_dict.map(function(e,i){return e[1]}).map(x => [x])

    console.log(sort_dict.slice(0,5))
    console.log(outputs);
    return (
      <div className="model__content">

       {/*
         * TODO: This is where you display your output.  You can show whatever you want, however
         * you want.  We've got a few examples, of text-based output, and of visualizing model
         * internals using heat maps.
         */}
        <div className="form__field">
          <label>Top 5 Predictions :</label>
          <table>
            <thead>
              <tr>
              <th>Label</th>
              <th>Probability</th>
              </tr>
            </thead>
            <tbody>
              {sort_dict.slice(0,5).map((x, _) => {
                return (
                  <tr>
                    <td>{x[0]}</td>
                    <td>{x[1]}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
        <Collapsible trigger="Model Visualisation">
        <Collapsible trigger="Categories HeatMap">
        <div className="form__field">
          <label>Predictions</label>
          {/* We like using Collapsible to show model internals; you can keep this or change it. */}
          <HeatMap xLabels={['']} yLabels={sorted_labels} data={sorted_predictions} xLabelWidth={xLabelWidth} />
        </div>
        </Collapsible>
        </Collapsible>

      </div>
    );
  }
}

export default ModelOutput;

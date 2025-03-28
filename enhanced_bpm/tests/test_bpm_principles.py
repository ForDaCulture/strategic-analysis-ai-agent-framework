import unittest
import json
import os

class TestBPMPrinciples(unittest.TestCase):
    """Test cases for the BPM principles JSON data."""

    @classmethod
    def setUpClass(cls):
        """Load the BPM principles JSON data once for all tests."""
        # Get the path to the JSON file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, '..', 'data', 'bpm_principles.json')
        
        # Load the JSON data
        with open(json_path, 'r', encoding='utf-8') as f:
            cls.bpm_data = json.load(f)

    def test_json_structure(self):
        """Test that the JSON has the expected top-level keys."""
        expected_keys = [
            'core_principles', 
            'methodologies', 
            'frameworks', 
            'maturity_models', 
            'performance_metrics',
            'implementation_best_practices',
            'common_challenges',
            'technology_enablers'
        ]
        
        for key in expected_keys:
            self.assertIn(key, self.bpm_data, f"Missing expected top-level key: {key}")

    def test_core_principles(self):
        """Test the structure and content of core principles."""
        principles = self.bpm_data['core_principles']
        
        # Check that we have the expected number of principles
        self.assertEqual(len(principles), 7, "Expected 7 core principles")
        
        # Check that each principle has the required fields
        required_fields = ['name', 'description', 'benefits', 'implementation_strategies']
        
        for principle in principles:
            for field in required_fields:
                self.assertIn(field, principle, f"Principle '{principle.get('name', 'Unknown')}' missing field: {field}")
            
            # Check that benefits and implementation_strategies are non-empty lists
            self.assertIsInstance(principle['benefits'], list, f"Benefits for '{principle['name']}' should be a list")
            self.assertGreater(len(principle['benefits']), 0, f"Benefits for '{principle['name']}' should not be empty")
            
            self.assertIsInstance(principle['implementation_strategies'], list, 
                                 f"Implementation strategies for '{principle['name']}' should be a list")
            self.assertGreater(len(principle['implementation_strategies']), 0, 
                              f"Implementation strategies for '{principle['name']}' should not be empty")

    def test_methodologies(self):
        """Test the structure and content of methodologies."""
        methodologies = self.bpm_data['methodologies']
        
        # Check that we have methodologies
        self.assertGreater(len(methodologies), 0, "Expected at least one methodology")
        
        # Check that each methodology has the required fields
        required_fields = ['name', 'description', 'key_concepts', 'tools', 'bpm_application']
        
        for methodology in methodologies:
            for field in required_fields:
                self.assertIn(field, methodology, 
                             f"Methodology '{methodology.get('name', 'Unknown')}' missing field: {field}")
            
            # Check that key_concepts and tools are non-empty lists
            self.assertIsInstance(methodology['key_concepts'], list, 
                                 f"Key concepts for '{methodology['name']}' should be a list")
            self.assertGreater(len(methodology['key_concepts']), 0, 
                              f"Key concepts for '{methodology['name']}' should not be empty")
            
            self.assertIsInstance(methodology['tools'], list, 
                                 f"Tools for '{methodology['name']}' should be a list")
            self.assertGreater(len(methodology['tools']), 0, 
                              f"Tools for '{methodology['name']}' should not be empty")

    def test_frameworks(self):
        """Test the structure and content of frameworks."""
        frameworks = self.bpm_data['frameworks']
        
        # Check that we have frameworks
        self.assertGreater(len(frameworks), 0, "Expected at least one framework")
        
        # Check that each framework has the required fields
        required_fields = ['name', 'description', 'components', 'bpm_application']
        
        for framework in frameworks:
            for field in required_fields:
                self.assertIn(field, framework, 
                             f"Framework '{framework.get('name', 'Unknown')}' missing field: {field}")
            
            # Check that components is a non-empty list
            self.assertIsInstance(framework['components'], list, 
                                 f"Components for '{framework['name']}' should be a list")
            self.assertGreater(len(framework['components']), 0, 
                              f"Components for '{framework['name']}' should not be empty")

    def test_maturity_models(self):
        """Test the structure and content of maturity models."""
        maturity_models = self.bpm_data['maturity_models']
        
        # Check that we have maturity models
        self.assertGreater(len(maturity_models), 0, "Expected at least one maturity model")
        
        # Check that each maturity model has the required fields
        required_fields = ['name', 'description', 'bpm_application']
        
        for model in maturity_models:
            for field in required_fields:
                self.assertIn(field, model, 
                             f"Maturity model '{model.get('name', 'Unknown')}' missing field: {field}")
            
            # Check that either levels or dimensions is present
            self.assertTrue('levels' in model or 'dimensions' in model, 
                           f"Maturity model '{model['name']}' should have either 'levels' or 'dimensions'")
            
            # If levels is present, check its structure
            if 'levels' in model:
                self.assertIsInstance(model['levels'], list, 
                                     f"Levels for '{model['name']}' should be a list")
                self.assertGreater(len(model['levels']), 0, 
                                  f"Levels for '{model['name']}' should not be empty")
                
                # Check first level has required fields
                if len(model['levels']) > 0:
                    first_level = model['levels'][0]
                    if isinstance(first_level, dict):
                        # Either 'level' or 'name' should be present to identify the level
                        self.assertTrue('level' in first_level or 'name' in first_level, 
                                       f"Level in '{model['name']}' missing both 'level' and 'name' identifiers")
                        # Description should always be present
                        self.assertIn('description', first_level, 
                                     f"Level in '{model['name']}' missing 'description'")

    def test_performance_metrics(self):
        """Test the structure and content of performance metrics."""
        metrics = self.bpm_data['performance_metrics']
        
        # Check that we have metrics categories
        self.assertGreater(len(metrics), 0, "Expected at least one metrics category")
        
        # Check that each category has the required fields
        for category in metrics:
            self.assertIn('category', category, "Metrics category missing 'category' field")
            self.assertIn('metrics', category, f"Metrics category '{category['category']}' missing 'metrics' field")
            
            # Check that metrics is a non-empty list
            self.assertIsInstance(category['metrics'], list, 
                                 f"Metrics for '{category['category']}' should be a list")
            self.assertGreater(len(category['metrics']), 0, 
                              f"Metrics for '{category['category']}' should not be empty")
            
            # Check each metric's structure
            for metric in category['metrics']:
                required_fields = ['name', 'description', 'calculation', 'improvement_strategies']
                for field in required_fields:
                    self.assertIn(field, metric, 
                                 f"Metric '{metric.get('name', 'Unknown')}' in '{category['category']}' missing field: {field}")
                
                # Check that improvement_strategies is a non-empty list
                self.assertIsInstance(metric['improvement_strategies'], list, 
                                     f"Improvement strategies for '{metric['name']}' should be a list")
                self.assertGreater(len(metric['improvement_strategies']), 0, 
                                  f"Improvement strategies for '{metric['name']}' should not be empty")

    def test_implementation_best_practices(self):
        """Test the structure and content of implementation best practices."""
        practices = self.bpm_data['implementation_best_practices']
        
        # Check that we have practice phases
        self.assertGreater(len(practices), 0, "Expected at least one implementation phase")
        
        # Check that each phase has the required fields
        for phase in practices:
            self.assertIn('phase', phase, "Implementation phase missing 'phase' field")
            self.assertIn('practices', phase, f"Implementation phase '{phase['phase']}' missing 'practices' field")
            
            # Check that practices is a non-empty list
            self.assertIsInstance(phase['practices'], list, 
                                 f"Practices for '{phase['phase']}' should be a list")
            self.assertGreater(len(phase['practices']), 0, 
                              f"Practices for '{phase['phase']}' should not be empty")

    def test_common_challenges(self):
        """Test the structure and content of common challenges."""
        challenges = self.bpm_data['common_challenges']
        
        # Check that we have challenges
        self.assertGreater(len(challenges), 0, "Expected at least one common challenge")
        
        # Check that each challenge has the required fields
        required_fields = ['challenge', 'description', 'mitigation_strategies']
        
        for challenge in challenges:
            for field in required_fields:
                self.assertIn(field, challenge, 
                             f"Challenge '{challenge.get('challenge', 'Unknown')}' missing field: {field}")
            
            # Check that mitigation_strategies is a non-empty list
            self.assertIsInstance(challenge['mitigation_strategies'], list, 
                                 f"Mitigation strategies for '{challenge['challenge']}' should be a list")
            self.assertGreater(len(challenge['mitigation_strategies']), 0, 
                              f"Mitigation strategies for '{challenge['challenge']}' should not be empty")

    def test_technology_enablers(self):
        """Test the structure and content of technology enablers."""
        enablers = self.bpm_data['technology_enablers']
        
        # Check that we have enablers
        self.assertGreater(len(enablers), 0, "Expected at least one technology enabler")
        
        # Check that each enabler has the required fields
        required_fields = ['name', 'description', 'capabilities', 'examples']
        
        for enabler in enablers:
            for field in required_fields:
                self.assertIn(field, enabler, 
                             f"Technology enabler '{enabler.get('name', 'Unknown')}' missing field: {field}")
            
            # Check that capabilities and examples are non-empty lists
            self.assertIsInstance(enabler['capabilities'], list, 
                                 f"Capabilities for '{enabler['name']}' should be a list")
            self.assertGreater(len(enabler['capabilities']), 0, 
                              f"Capabilities for '{enabler['name']}' should not be empty")
            
            self.assertIsInstance(enabler['examples'], list, 
                                 f"Examples for '{enabler['name']}' should be a list")
            self.assertGreater(len(enabler['examples']), 0, 
                              f"Examples for '{enabler['name']}' should not be empty")

    def test_json_validity(self):
        """Test that all strings in the JSON are properly formatted."""
        # Convert the JSON back to a string and then parse it again to check for formatting issues
        json_str = json.dumps(self.bpm_data)
        try:
            json.loads(json_str)
        except json.JSONDecodeError as e:
            self.fail(f"JSON is not properly formatted: {e}")

    def test_cross_references(self):
        """Test that there are no duplicate names within each category."""
        # Check for duplicate principle names
        principle_names = [p['name'] for p in self.bpm_data['core_principles']]
        self.assertEqual(len(principle_names), len(set(principle_names)), 
                        "Duplicate core principle names found")
        
        # Check for duplicate methodology names
        methodology_names = [m['name'] for m in self.bpm_data['methodologies']]
        self.assertEqual(len(methodology_names), len(set(methodology_names)), 
                        "Duplicate methodology names found")
        
        # Check for duplicate framework names
        framework_names = [f['name'] for f in self.bpm_data['frameworks']]
        self.assertEqual(len(framework_names), len(set(framework_names)), 
                        "Duplicate framework names found")
        
        # Check for duplicate maturity model names
        model_names = [m['name'] for m in self.bpm_data['maturity_models']]
        self.assertEqual(len(model_names), len(set(model_names)), 
                        "Duplicate maturity model names found")
        
        # Check for duplicate technology enabler names
        enabler_names = [e['name'] for e in self.bpm_data['technology_enablers']]
        self.assertEqual(len(enabler_names), len(set(enabler_names)), 
                        "Duplicate technology enabler names found")

if __name__ == '__main__':
    unittest.main()
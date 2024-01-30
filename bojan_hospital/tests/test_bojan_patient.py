from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestBojanPatient(TransactionCase):

    def test_create_patient(self):
        patient_data = {'name': 'John', 'surename': 'Doe', 'custom_field': None}
        patient = self.env['bojan.patient'].create(patient_data)
        with self.assertRaises(ValidationError, msg="Expected validation error for empty 'custom_field'."):
            patient.check_access_rule('create')

    def test_update_patient(self):
        patient = self.env['bojan.patient'].create({'name': 'Alice', 'surename': 'Smith', 'custom_field': 42})
        patient.write({'name': 'NewName'})
        print("Test update_patient: Patient updated. New name:", patient.name)
        print("Test update_patient: Patient surename:", patient.surename)
        self.assertEqual(patient.name, 'NewName', "Patient update failed.")
        self.assertEqual(patient.surename, 'Smith', "Patient update failed.")

    def test_invalid_patient(self):
        with self.assertRaises(ValidationError, msg="Expected validation error for empty 'custom_field'."):
            self.env['bojan.patient'].create({'name': '', 'surename': 'InvalidSurename', 'custom_field': None})
        print("Test invalid_patient: Validation error expected. Test passed.")

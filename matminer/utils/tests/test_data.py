import unittest
from math import isnan
from unittest import TestCase

from pymatgen.core import Element
from pymatgen.core.periodic_table import Specie

from matminer.utils.data import (
    DemlData,
    IUCrBondValenceData,
    MagpieData,
    MatscholarElementData,
    MEGNetElementData,
    MixingEnthalpy,
    OpticalData,
    PymatgenData,
    TransportData,
)


class TestDemlData(TestCase):
    """Tests for the DemlData Class"""

    def setUp(self):
        self.data_source = DemlData()

    def test_get_property(self):
        self.assertAlmostEqual(
            -4.3853,
            self.data_source.get_elemental_property(Element("Bi"), "mus_fere"),
            4,
        )
        self.assertEqual(
            59600,
            self.data_source.get_elemental_property(Element("Li"), "electron_affin"),
        )
        self.assertAlmostEqual(
            2372300,
            self.data_source.get_elemental_property(Element("He"), "first_ioniz"),
        )
        self.assertAlmostEqual(
            sum([2372300, 5250500]),
            self.data_source.get_charge_dependent_property_from_specie(Specie("He", 2), "total_ioniz"),
        )
        self.assertAlmostEqual(
            18.6,
            self.data_source.get_charge_dependent_property_from_specie(Specie("V", 3), "xtal_field_split"),
        )

    def test_get_oxidation(self):
        self.assertEqual([1], self.data_source.get_oxidation_states(Element("Li")))


class TestMagpieData(TestCase):
    def setUp(self):
        self.data_source = MagpieData()

    def test_get_property(self):
        self.assertAlmostEqual(
            9.012182,
            self.data_source.get_elemental_property(Element("Be"), "AtomicWeight"),
        )

    def test_get_oxidation(self):
        self.assertEqual([-4, 2, 4], self.data_source.get_oxidation_states(Element("C")))


class TestPymatgenData(TestCase):
    def setUp(self):
        self.data_source = PymatgenData()

    def test_get_property(self):
        self.assertAlmostEqual(
            9.012182,
            self.data_source.get_elemental_property(Element("Be"), "atomic_mass"),
        )
        self.assertAlmostEqual(
            1.26,
            self.data_source.get_charge_dependent_property(Element("Ac"), 3, "ionic_radii"),
        )

    def test_get_oxidation(self):
        self.assertEqual((3,), self.data_source.get_oxidation_states(Element("Nd")))
        self.data_source.use_common_oxi_states = False
        self.assertEqual((2, 3), self.data_source.get_oxidation_states(Element("Nd")))


class TestMatScholarData(TestCase):
    def setUp(self):
        self.data_source = MatscholarElementData()

    def test_get_property(self):
        embedding_cu = self.data_source.get_elemental_property(Element("Cu"), "embedding 3")
        self.assertAlmostEqual(0.028666902333498, embedding_cu)

        with self.assertRaises(KeyError):
            self.data_source.get_elemental_property(Element("Db"), "embedding 9")


class TestMEGNetData(TestCase):
    def setUp(self):
        self.data_source = MEGNetElementData()

    def test_get_property(self):
        embedding_cu = self.data_source.get_elemental_property(Element("Cu"), "embedding 1")
        self.assertAlmostEqual(0.18259364366531372, embedding_cu)

        # MEGNet embeddings have element data for elements 1-94, plus 0 for
        # "dummy" atoms.
        embedding_md = self.data_source.get_elemental_property(Element("Md"), "embedding 1")
        self.assertAlmostEqual(-0.044910576194524765, embedding_md)

        embedding_dummy = self.data_source.all_element_data["Dummy"]["embedding 1"]
        self.assertAlmostEqual(-0.044910576194524765, embedding_dummy)


class TestMixingEnthalpy(TestCase):
    def setUp(self):
        self.data = MixingEnthalpy()

    def test_get_data(self):
        self.assertEqual(-27, self.data.get_mixing_enthalpy(Element("H"), Element("Pd")))
        self.assertEqual(-27, self.data.get_mixing_enthalpy(Element("Pd"), Element("H")))
        self.assertTrue(isnan(self.data.get_mixing_enthalpy(Element("He"), Element("H"))))


class TestIUCrBondValenceData(TestCase):
    def setUp(self):
        self.data = IUCrBondValenceData()

    def test_get_data(self):
        nacl = self.data.get_bv_params("Na", "Cl", 1, -1)
        self.assertAlmostEqual(nacl["Ro"], 2.15)


class TestOpticalData(TestCase):
    def setUp(self):
        self.data_source = OpticalData()

    def test_get_data(self):
        au_r = self.data_source.get_elemental_property(elem="Au", property_name="R_400.0")
        self.assertAlmostEqual(au_r, 0.25489326484782054)
        ag_n = self.data_source.get_elemental_property(elem="Ag", property_name="n_600.0")
        self.assertAlmostEqual(ag_n, 0.13644859985917585)
        c_k = self.data_source.get_elemental_property(elem="C", property_name="k_760.0")
        self.assertAlmostEqual(c_k, 0.7462931865379264)


class TestTransportData(TestCase):
    def setUp(self):
        self.data_source = TransportData()

    def test_get_data(self):
        ca_mn = self.data_source.get_elemental_property(elem="Ca", property_name="m_n")
        self.assertAlmostEqual(ca_mn, 0.000279554)
        cr_sigmap = self.data_source.get_elemental_property(elem="Cr", property_name="sigma_p")
        self.assertAlmostEqual(cr_sigmap, 205569.89838499163)
        cu_kappan = self.data_source.get_elemental_property(elem="Cu", property_name="kappa_n")
        self.assertAlmostEqual(cu_kappan, 1814544.75663, places=5)


if __name__ == "__main__":
    unittest.main()

import unittest

import jax
from parax.testing import PipelineBasicTest


class AutoSlicingTest(PipelineBasicTest):

    # FIXME(zhuohan): The following test fails because stage slicing
    #   in XLA will move the stages around and thus don't have correct order
    #   if stages on a same mesh doesn't have dependecies. Need to fix this
    #   in stage slicing in XLA.
    @unittest.skip("Some issue in XLA")
    def test_mlp_auto_layer_slicing(self):
        self.run_mlp(manual_pipeline_layer=False)

    def test_2_layer_bert_auto_layer_slicing(self):
        self.run_n_layer_bert(n_layers=2, manual_pipeline_layer=False)

    @unittest.skipIf(jax.device_count('gpu') < 8, "no enough device")
    def test_8_layer_bert_auto_layer_slicing(self):
        self.run_n_layer_bert(n_layers=8, manual_pipeline_layer=False)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(AutoSlicingTest('test_mlp_auto_layer_slicing'))
    suite.addTest(AutoSlicingTest('test_2_layer_bert_auto_layer_slicing'))
    suite.addTest(AutoSlicingTest('test_8_layer_bert_auto_layer_slicing'))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
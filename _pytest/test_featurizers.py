import numpy as np
import os


def test_spacy():
    def test_sentence(sentence, language, _ref):
        import spacy
        from rasa_nlu.featurizers.spacy_featurizer import SpacyFeaturizer
        nlp = spacy.load(language, tagger=False, parser=False)
        doc = nlp(sentence)
        ftr = SpacyFeaturizer(nlp)
        vecs = ftr.create_bow_vecs([sentence])
        assert np.allclose(doc.vector[:5], _ref, atol=1e-5)
        assert np.allclose(vecs[0], doc.vector, atol=1e-5)

    test_sentence(u"hey how are you today",
                  'en',
                  _ref=np.array([0.02188552, 0.00557156, -0.01211646, -0.00866477, 0.02179166]))

    test_sentence(u"hey wie geht es dir",
                  'de',
                  _ref=np.array([0.02188552, 0.00557156, -0.01211646, -0.00866477, 0.02179166]))


def test_mitie():
    from rasa_nlu.featurizers.mitie_featurizer import MITIEFeaturizer
    filename = os.environ.get('MITIE_FILE')
    if (filename and os.path.isfile(filename)):
        ftr = MITIEFeaturizer(os.environ.get('MITIE_FILE'))
        sentence = "Hey how are you today"
        vecs = ftr.create_bow_vecs([sentence])
        assert np.allclose(vecs[0][:5], np.array([0., -4.4551446, 0.26073121, -1.46632245, -1.84205751]), atol=1e-5)

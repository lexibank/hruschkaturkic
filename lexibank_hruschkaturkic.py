from pathlib import Path
from clldutils.misc import slug
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank import Concept, Language
from pylexibank.forms import FormSpec
from pylexibank import progressbar
import attr

#@attr.s
#class CustomConcept(Concept):
#    Chinese_Gloss = attr.ib(default=None)


#@attr.s
#class CustomLanguage(Language):
#    Location = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "hruschkaturkic"

    def cmd_makecldf(self, args):

        mapper = {
                row["Grapheme"]: [row["IPA"], row["IPAInSource"]] for row in self.etc_dir.read_csv(
                "orthography.tsv", delimiter="\t",
                dicts=True)}
        data = {}
        for taxon, string in progressbar(
                self.raw_dir.read_csv('TurkicFullBoundaries.txt', delimiter="\t"),
                desc='reading data'
                ):
            out = []
            for char in string:
                if char == '-':
                    out += ['-']
                else:
                    out += [char]
            out = ' '.join(out)
            data[taxon] = [''.join(x).strip().split() for x in out.split(':')]

        for i in range(len(data[taxon])):
            args.writer.add_concept(
                    ID="word-{0}".format(i+1),
                    Name="Etymon {0}".format(i+1)
                    )

        for language in progressbar(self.languages):
            args.writer.add_language(
                    ID=language["ID"],
                    Name=language["Name"],
                    Glottocode=language["Glottocode"] or ""
                    )
            for i, word in enumerate(data[language["ID"]]):
                alignment = [mapper.get(t, [t])[0] for t in word]
                tokens = [t for t in alignment if t != "-"]
                value = [mapper.get(t, [t, t])[1] for t in word]
                if tokens:
                    lex = args.writer.add_form_with_segments(
                        Language_ID=language["ID"],
                        Parameter_ID="word-{0}".format(i+1),
                        Value="".join(value),
                        Form=" ".join(word),
                        Segments=tokens,
                        Cognacy=i+1
                        )
                    args.writer.add_cognate(
                        lexeme=lex,
                        Cognateset_ID=i+1,
                        Alignment=alignment,
                        )



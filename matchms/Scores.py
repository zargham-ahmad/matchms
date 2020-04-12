from numpy import empty, argsort, unravel_index, hstack, vstack


class Scores:
    """An example docstring for a class definition."""
    def __init__(self, queries, references, similarity_function, scores=None):
        """An example docstring for a constructor."""
        self.queries = hstack(queries)
        self.references = vstack(references)
        self.similarity_function = similarity_function
        if scores is None:
            self.scores = empty([len(self.references),
                                 len(self.queries)])
        else:
            self.scores = scores

    def __str__(self):
        return self.scores.__str__()

    def calculate(self):
        """An example docstring for a method."""
        for i_ref, reference in enumerate(self.references.flatten()):
            for i_query, query in enumerate(self.queries.flatten()):
                self.scores[i_ref][i_query] = self.similarity_function(query, reference)
        return self

    def sort(self, kind="quicksort"):
        """An example docstring for a method."""
        sortorder = argsort(self.scores.flatten(), kind=kind)[::-1]
        # pylint: disable=unbalanced-tuple-unpacking
        r, c = unravel_index(sortorder, self.scores.shape)
        return vstack(self.queries[c]), self.references[r], vstack(self.scores[r, c])

    def top(self, n, kind="quicksort", omit_self_comparisons=True):

        queries_sorted, references_sorted, scores_sorted = self.sort(kind=kind)

        if omit_self_comparisons:
            zipped = zip(queries_sorted, references_sorted, scores_sorted)
            self_comparisons_omitted = [(q, r, s) for q, r, s in zipped if q != r]
            return \
                vstack([q for q, _, _ in self_comparisons_omitted[:n]]),\
                vstack([r for _, r, _ in self_comparisons_omitted[:n]]),\
                vstack([s for _, _, s in self_comparisons_omitted[:n]])

        return queries_sorted[:n], references_sorted[:n], scores_sorted[:n]

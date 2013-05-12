The following is an earlier unfinished attempt at putting down my
ideas on metadata.

---

I use "metadata" here to refer very generally to all those descriptors
that are associated with each value in a collection (or set) of values
so as to render this collection/set interpretable as "data".


When thinking about "metadata" it is useful to distinguish a subset of
it, which I will refer to as "model metadata", consisting of those
items that are indispensable if one is to map the "bare" values onto
the scientific picture that informs the data gathering.  As a rule of
thumb, the model metadata consists of all those pieces of information
that will label the figures, or parts thereof, at the time of
describing the experiment’s findings to a scientific audience.


For example, consider an experiment, [...].  Here, the model metadata
includes the name of the model variable that the measurement
represents, the units (possibly "none") in which the measurement is
expressed, difference between the time of treatment and the time of
measurement.


Non-model metadata, on the other hand, describe contingent details of
the experimental conditions.  If two different set out to conduct
independent replicates of the same experimental design, they two
experiments should have identical model metadata (not only the same
model metadata factors, but also the same levels for those factors).
In contrast, their non-model metadata will have, almost always,
different values.


One suggestive name for the non-model metadata is "confounders",
since, by definition, all non-model metadata represents some potential
confounder in the subsequent analysis.  The downside of this
terminology, however, is that it implies that the only purpose for
collecting non-model metadata is to take into account the effect of
confounders in the subsequent analysis.  In fact, there are many other
reasons for collecting non-model metadata, such, troubleshooting
experimental problems, optimizing experimental protocols, and
conducting "forensic" investigations of published results.


Continuing with the earlier example, the following would all be
classified as "confounders" (in the generalized sense described
above): the plate number-well coordinates of the sample from which the
measurement was obtained, the batch number of the culture medium, the
date of the measurement, etc.
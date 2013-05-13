* some basic definitions/distinctions

* associated with each measurement (or quantum of "data") are several
attributes that we refer to collectively as "metadata".

* it is useful to classify metadata according to their general
purpose, resulting in the following three broad categories (roughly in
order of decreasing intrinsic significance/scope of
reference/"half-life")

** model metadata (aka "factors"): these correspond to the variables
   (or transforms thereof) of the scientific model(s) behind the
   experiment; (modeling)
** confounder metadata (aka "confounders"): experimental details;
   useful for forensics, troubleshooting, optimization; (LIMS)
** relational reference metadata: internal indices used to relate data
   points to each other; (RDBM)

* parallel to the model/confounder distinction above, is a distinction
  between ideal and actual entities: in some contexts the name
  "lapatinib", for example, is a reference to a certain compound "in
  general", whereas in other context, the same name refers to a
  specific reagent supplied by a specific vendor, having a batch
  number, used in a specific experiment, at a specific date, etc.

---

   Factors are variables in the model that motivates the experiment,
   while confounders are variables that are extraneous to this model.
   Operationally, confounders are distinguished from factors in that
   the former are the part of the available information that the
   subsequent analysis either ignores or aims to "analyze away"
   (e.g. by averaging).

---

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
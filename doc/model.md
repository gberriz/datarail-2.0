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

Heuristic:
WORK FROM CONCRETE TO GENERAL, AND FROM UNSTRUCTURED TO STRUCTURED.

Let's start with an example.  Consider the following hypothetical
experiment: a panel of... (???)

---

Terminology

The Cartesian product of the finite sets A1, A2, …, An is the set of
all tuples (a1, a2, …, an), where ai ∈ Ai, for all i ∈ {1, 2, …, n}.

For example, the Cartesian product of the sets A1 = {0, 1} and A2 =
{a, b, c} is the set {(0, a), (0, b), (0, c), (1, a), (1, b), (1, c)}.

A factor (or more precisely, "factor set") is a finite set of
"allowable values".  Factors correspond to the experimenter-set
variables that specify the conditions probed by the experiment.

As we use it here, a cube may be defined most succinctly (and
abstractly) as a function whose domain is a Cartesian product of
factors and whose range is a Cartesian product of measurement spaces.

---

Convention for describing data cubes:

When describing a regular multidimensional data cube, there is some
ambiguity in how one specifies the cube's shape, since an
n-dimensional cube of scalars can also be understood as an (n -
1)-dimensional cube of vectors, or as an (n - k)-dimensional vector of
k-dimensional arrays, or (if we apply this idea recursively) as any
one of a large number of multilevel representations.  For any
particular data cube, some of these alternative descriptions will be
more meaningful than others, but even for a single data cube, the
optimal choice will depend on unpredictable contingencies such as the
specific analysis being performed, or the analyst's subjective
perception of the data contained in the cube.


With this caveat in mind, we choose dimensions for cubes and their
values so as to make the degree of "semantic compatibility" among the
cubes as apparent as possible to the analyst.


For example, suppose that we have two types of data, one being scalar
and the other one being a 4-dimensional vector, associated with each
sample in a dataset.  Suppose also that we can represent the set of
all samples as a 5-dimensional space.

The cubes corresponding to these two types of data could be seen as
two multidimensional arrays, with dimensions 5 and 6 respectively, of
scalars values.

Alternatively, they could be seen as two 5-dimensional arrays,
containing scalars and 4-dimensional vectors, respectively, as values.
The latter description reminds the analyst that the two cubes are
"semantically compatible" (their factors and their levels have
identical meaning).

---

For example, consider two cubes of data, A and B, containing different
data values for the same collection of samples.  Suppose that we can
represent the set of all samples as a 5-dimensional space, and that
cube A consists of scalars...

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


---

1. dictionary
2. compatibility info (which cube-combining operations are valid?)
3. experiment
1. methods
2. cubes
1. processing
2. factors
1. unit
2. levels
3. missing values (taxonomy; policies; semantics)
________________


EXPERIMENTS
Fluorescence microscopy
1. growth factor series (GF)
2. cytokine series (CK)
Methods
Cubes
GF: 
1. growth factor series (GF)
2. cytokine series (CK)
ELISA
Methods
Cubes


Protein profiling
Methods
Cubes




[with antibodies of the specificites given below, and at various
timepoints after stimulation with various concentrations of ligands]
1. pAkt
2. pErk
1. Protein profiling

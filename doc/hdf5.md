The only documentation I can find at the moment of the HDF5 format is

* what is given on points 4, 7, and 8 of the section DATA PROCESSING
in http://sorger.private.openwetware.org/wiki/Overview.

* the notes below.

---

Heuristic: work from concrete to general; work from unstructured to
structured


Terminology
Let’s start with an example.  Consider the following hypothetical
experiment: a panel of


The Cartesian product of the finite sets A1, A2, …, An is the set of
all tuples (a1, a2, …, an), where ai ∈ Ai, for all i ∈ {1, 2, …, n}.
For example, the Cartesian product of the sets A1 = {0, 1} and A2 =
{a, b, c} is the set {(0, a), (0, b), (0, c), (1, a), (1, b), (1, c)}.


A factor is one of the independent variables


(or more precisely, factor set) is a finite set of 


As we use it here, a cube may be defined most succinctly (and
abstractly) as a function whose domain is a Cartesian product of
factor


Convention for describing data cubes:


When describing a regular multidimensional data cube, there is some
ambiguity in how one specifies the cube’s shape, since an
n-dimensional cube of scalars can also be understood as an (n -
1)-dimensional cube of vectors, or as an (n - k)-dimensional vector of
k-dimensional arrays, or (if we apply this idea recursively) as any
one of a large number of multilevel representations.  For any
particular data cube, some of these alternative descriptions will be
more meaningful than others, but even for a single data cube, the
optimal choice will depend on unpredictable contingencies such as the
specific analysis being performed, or the analyst’s subjective
perception of the data contained in the cube.


With this caveat in mind, we choose dimensions for cubes and their
values so as the degree of "semantic compatibility" among the cubes as
apparent as possible to the analyst.


For example, suppose that we have two types of data, one being scalar
and the other one being a 4-dimensional vector, associated with each
sample in a dataset.  Suppose also that we can represent the set of
all samples as a 5-dimensional space.  The cubes corresponding to
these two types of data could be seen as two multidimensional arrays,
with dimensions 5 and 6 respectively, of scalars values.
Alternatively, they could be seen as two 5-dimensional arrays,
containing scalars and 4-dimensional vectors, respectively, as values.
The latter description reminds the analyst that the two cubes are
"semantically compatible" (their factors and their levels have
identical meaning).


For example, consider two cubes of data, A and B, containing different
data values for the same collection of samples.  Suppose that we can
represent the set of all samples as a 5-dimensional space, and that
cube A consists of scalars


.
├── confounders
│   ├── CK
│   │   ├── data
│   │   └── labels
│   ├── GF
│   │   ├── data
│   │   └── labels
│   └── keymap
├── from_IR
│   ├── CK
│   │   ├── data
│   │   └── labels
│   └── GF
│           ├── data
│           └── labels
└── from_IR_w_zeros
        ├── CK
        │   ├── data
        │   └── labels
        └── GF
            ├── data
            └── labels




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
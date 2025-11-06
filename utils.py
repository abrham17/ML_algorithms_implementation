import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from hyperon import MeTTa, ValueAtom, ExpressionAtom, AtomKind, OperationAtom, E, S, V, Atom
from hyperon.ext import register_atoms
import numpy.linalg as la

# Global variables to store model data
models = None
probs_list = None
X_val = None
y_val = None

def initialize_models():
    """Initialize and train the base models"""
    global models, probs_list, X_val, y_val
    
    # Load and prepare data
    X, y = load_iris(return_X_y=True)
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_val = scaler.transform(X_val)

    # Train models
    models = [
        LogisticRegression(max_iter=200),
        RandomForestClassifier(n_estimators=50, random_state=0),
        GradientBoostingClassifier(n_estimators=50, random_state=0),
        KNeighborsClassifier(n_neighbors=5),
        SVC(probability=True, gamma="scale", random_state=0),
    ]
    
    probs_list = []
    for m in models:
        m.fit(X_train, y_train)
        probs_list.append(m.predict_proba(X_val))
    return probs_list
def ensemble_probs_from_w(probs_list, w):
    """Calculate ensemble probabilities from weights"""
    w = np.clip(w, 0.0, 1.0)
    w_sum = max(w.sum(), 1e-12)
    weighted = sum(w_i * p_i for w_i, p_i in zip(w, probs_list))
    return weighted / w_sum

def fitness(w):
    """Calculate fitness (1 - accuracy) for given weights"""
    probs = ensemble_probs_from_w(probs_list, w)
    preds = np.argmax(probs, axis=1)
    acc = accuracy_score(y_val, preds)
    return 1.0 - acc  # CMA-ES minimizes this

# Fixed atom conversion functions
def atom_to_np(atom):
    """Convert MeTTa atom to numpy array or scalar"""
    if hasattr(atom, 'get_children'):  # Expression atom
        children = atom.get_children()
        return np.array([atom_to_np(ch) for ch in children])
    elif hasattr(atom, 'get_object'):  # Grounded atom
        obj = atom.get_object()
        if hasattr(obj, 'value'):
            return obj.value
        elif hasattr(obj, 'content'):
            return obj.content
        else:
            return obj
    elif hasattr(atom, 'get_name'):  # Symbol or Variable
        try:
            return float(atom.get_name())
        except ValueError:
            return atom.get_name()
    else:
        return atom

def list_to_atom(lst):
    """Convert Python list/number to MeTTa atom"""
    if isinstance(lst, (int, float)):
        return ValueAtom(lst)
    elif isinstance(lst, (list, np.ndarray)):
        # Convert each element recursively and create expression
        atom_list = []
        for item in lst:
            atom_list.append(list_to_atom(item))
        return E(*atom_list)
    else:
        raise ValueError(f"Unsupported type for conversion: {type(lst)}")

# Python functions that will be called from MeTTa
def py_fitness(*weights_list):
    """Python fitness function called from MeTTa"""
    weights = np.array(weights_list).flatten()
    return float(fitness(weights))


def py_multivariate_normal(mean, cov, sigma):
    """Python multivariate normal sampling"""
    mean_np = np.array(mean)
    cov_np = np.array(cov)
    sigma_np = float(sigma)
    sample = np.random.multivariate_normal(mean_np, sigma_np**2 * cov_np)
    return sample.tolist()

def py_outer_product(v1, v2):
    """Python outer product"""
    v1_np = np.array(v1)
    v2_np = np.array(v2)
    outer = np.outer(v1_np, v2_np)
    return outer.tolist()

def py_mat_mul(mat, vec):
    """Python matrix multiplication"""
    mat_np = np.array(mat)
    vec_np = np.array(vec)
    result = np.dot(mat_np, vec_np)
    return result.tolist()

def py_inv_sqrt(mat):
    """Python inverse square root of matrix"""
    mat_np = np.array(mat)
    vals, vecs = la.eigh(mat_np)
    vals = np.maximum(vals, 0)
    inv_sqrt_vals = 1.0 / np.sqrt(vals + 1e-10)
    D = np.diag(inv_sqrt_vals)
    inv_sqrt_mat = vecs @ D @ vecs.T
    return inv_sqrt_mat.tolist()

def identity_matrix(n):
    """Python identity matrix"""
    n_int = int(n)
    eye = np.eye(n_int)
    return eye.tolist()

# Fixed pyModule functions
def pyModule(metta: MeTTa, name: Atom, *args: Atom):
    """Generic Python module connector"""
    payload_expression = args[0]
    actual_arg_atoms = payload_expression.get_children()
    functionName = str(name)
    handler_args = [atom_to_np(arg) for arg in actual_arg_atoms]

    # Run the function
    result = globals()[functionName](*handler_args)
    return [ValueAtom(result)]

def pyModuleX(metta: MeTTa, name: Atom, *args: Atom):
    """Generic Python module connector with expression result"""
    payload_expression = args[0]
    actual_arg_atoms = payload_expression.get_children()
    functionName = str(name)
    handler_args = [atom_to_np(arg) for arg in actual_arg_atoms]

    # Run the function
    result = globals()[functionName](*handler_args)
    return [list_to_atom(result)]

@register_atoms(pass_metta=True)
def pyModule_(metta):
    return {
        "pyModule": OperationAtom(
            "pyModule",
            lambda name, *payload: pyModule(metta, name, *payload),
            unwrap=False,
        )
    }

@register_atoms(pass_metta=True)
def pyModule_x(metta):
    return {
        "pyModuleX": OperationAtom(
            "pyModuleX",
            lambda name, *payload: pyModuleX(metta, name, *payload),
            unwrap=False,
        )
    }

initialize_models()
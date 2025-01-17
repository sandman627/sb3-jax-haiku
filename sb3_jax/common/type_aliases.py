"""Common aliases for type hints"""

from enum import Enum
from typing import Any, Callable, Dict, List, NamedTuple, Tuple, Union

import gym
import numpy as np
import jax.numpy as jnp

from stable_baselines3.common import callbacks, vec_env

GymEnv = Union[gym.Env, vec_env.VecEnv]
GymObs = Union[Tuple, Dict[str, Any], np.ndarray, int]
GymStepReturn = Tuple[GymObs, float, bool, Dict]
JnpDict = Dict[Union[str, int], jnp.ndarray]
OptimizerStateDict = Dict[str, Any]
MaybeCallback = Union[None, Callable, List[callbacks.BaseCallback], callbacks.BaseCallback]

# A schedule takes the remaining progress as input
# and ouputs a scalar (e.g. learning rate, clip range, ...)
Schedule = Callable[[float], float]


class RolloutBufferSamples(NamedTuple):
    observations: jnp.ndarray
    actions: jnp.ndarray
    old_values: jnp.ndarray
    old_log_prob: jnp.ndarray
    advantages: jnp.ndarray
    returns: jnp.ndarray


class ReplayBufferSamples(NamedTuple):
    observations: jnp.ndarray
    actions: jnp.ndarray
    next_observations: jnp.ndarray
    dones: jnp.ndarray
    rewards: jnp.ndarray


class TrajectoryBufferSamples(NamedTuple):
    observations: jnp.ndarray
    actions: jnp.ndarray
    rewards: jnp.ndarray
    dones: jnp.ndarray
    returns_to_go: jnp.ndarray
    timesteps: jnp.ndarray
    masks: jnp.ndarray


class RolloutReturn(NamedTuple):
    episode_timesteps: int
    n_episodes: int
    continue_training: bool


class TrainFrequencyUnit(Enum):
    STEP = "step"
    EPISODE = "episode"


class TrainFreq(NamedTuple):
    frequency: int
    unit: TrainFrequencyUnit  # either "step" or "episode"

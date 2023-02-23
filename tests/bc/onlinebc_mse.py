import os
os.environ['XLA_PYTHON_CLIENT_PREALLOCATE'] = 'true'
os.environ['XLA_PYTHON_CLIENT_MEM_FRACTION'] = '0.8'
import gym

from stable_baselines3.common import env_util, vec_env
from sb3_jax import OnlineBC
from sb3_jax.bc.policies import MlpPolicy
from sb3_jax.common.evaluation import evaluate_policy
from sb3_jax.common.norm_layers import RunningNormLayer
from sb3_jax.common.buffers import ReplayBuffer


env_train = env_util.make_vec_env('Swimmer-v3')
env_train = vec_env.VecNormalize(env_train, norm_obs=False, norm_reward=True)
env_eval = env_util.make_vec_env('Swimmer-v3')

# Load Buffer
buff = ReplayBuffer(
    buffer_size=2_500_000,
    observation_space=env_train.observation_space,
    action_space=env_train.action_space,
    n_envs=1,
    optimize_memory_usage=True,
)
buff = buff.load(path='../data/replay_buffer.pkl')

# Make BC
bc = OnlineBC(
    policy=MlpPolicy,
    env=env_train,
    learning_starts=0,
    learning_rate=3e-4,
    batch_size=64,
    loss_type='mse',
    verbose=1,
    wandb_log="onlinebc_test",
    policy_kwargs=dict(
        net_arch=[64, 64],
        normalization_class=RunningNormLayer,
        use_dist=False,
    )
)
# should replace the replay buffer to the loadded one
bc.replay_buffer = buff
print(bc.replay_buffer.observations[0][0])

mean_reward, _ = evaluate_policy(bc, env_eval, n_eval_episodes=10, max_ep_length=200)
print(f"Before Learning: {mean_reward}")
bc.learn(total_timesteps=10_000, log_interval=1) # log interval per episode ...
mean_reward, _ = evaluate_policy(bc, env_eval, n_eval_episodes=10, max_ep_length=200)
print(f"After Learning: {mean_reward}")
bc.save(path='../model/bc')

# Loading Model
_bc = OnlineBC(
    policy=MlpPolicy,
    env=env_train,
    policy_kwargs=dict(
        net_arch=[64, 64],
        normalization_class=RunningNormLayer,
        use_dist=False,
    )
)
_bc = _bc.load(path='../model/bc') 
mean_reward, _ = evaluate_policy(_bc, env_eval, n_eval_episodes=10, max_ep_length=200)
print(f"Load Learning: {mean_reward}")

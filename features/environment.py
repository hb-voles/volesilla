"""Behave environment"""

import os
import shutil
import tempfile
import subprocess


def before_all(context):
    """Setup environemnt before all behaves"""

    context.main_test_dir = tempfile.mkdtemp(prefix='vls_behave-')

    context.base_wd = os.getcwd()


def after_all(context):
    """Clean up environment after all behaves"""

    try:
        is_debug = True if os.environ['VLS_BEHAVE_DEBUG'] else False
    except KeyError:
        is_debug = False

    if is_debug:
        print('DEBUG: Behave test dir is [{}]'.format(context.main_test_dir))
    else:
        shutil.rmtree(context.main_test_dir)
        context.main_test_dir = None


def before_feature(context, feature):
    """Setup before each feature"""
    context.feature_test_dir = os.path.join(context.main_test_dir, feature.name.replace(' ', '_'))

    if not os.path.exists(context.feature_test_dir):
        os.makedirs(context.feature_test_dir)


def before_scenario(context, scenario):
    """Setup environment before each scenario"""
    context.scenario_test_dir = os.path.join(
        context.feature_test_dir, scenario.name.replace(' ', '_'))

    if not os.path.exists(context.scenario_test_dir):
        os.makedirs(context.scenario_test_dir)

    subprocess.check_call(['python', 'volesilla_utils.py', 'db_init', '-t',
                           context.scenario_test_dir, 'volesilla_test.db'])
    os.chdir(context.scenario_test_dir)

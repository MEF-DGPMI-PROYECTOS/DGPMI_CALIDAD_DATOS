#!
# # Create Your Checkpoint
# Use this notebook to configure a new Checkpoint and add it to your project:
#
# **Checkpoint Name**: `ckpt_{table_name}`

# In[12]:
from ruamel.yaml import YAML
import great_expectations as ge
from pprint import pprint

yaml = YAML()
context = ge.get_context()
# # Create a Checkpoint Configuration
#
# **If you are new to Great Expectations or the Checkpoint feature**, you should start with SimpleCheckpoint because it includes default configurations like a default list of post validation actions.
#
# In the cell below we have created a sample Checkpoint configuration using **your configuration** and **SimpleCheckpoint** to run a single validation of a single Expectation Suite against a single Batch of data.
#
# To keep it simple, we are just choosing the first available instance of each of the following items you have configured in your Data Context:
# * Datasource
# * DataConnector
# * DataAsset
# * Partition
# * Expectation Suite
#
# Of course this is purely an example, you may edit this to your heart's content.
#
# **My configuration is not so simple - are there more advanced options?**
#
# Glad you asked! Checkpoints are very versatile. For example, you can validate many Batches in a single Checkpoint, validate Batches against different Expectation Suites or against many Expectation Suites, control the specific post-validation actions based on Expectation Suite / Batch / results of validation among other features. Check out our documentation on Checkpoints for more details and for instructions on how to implement other more advanced features including using the **Checkpoint** class:
# - https://docs.greatexpectations.io/docs/reference/checkpoints_and_actions
# - https://docs.greatexpectations.io/docs/guides/validation/checkpoints/how_to_create_a_new_checkpoint
# - https://docs.greatexpectations.io/docs/guides/validation/checkpoints/how_to_configure_a_new_checkpoint_using_test_yaml_config

# In[2]:
table_name = "tr_proy_ano"
my_checkpoint_name = "ckpt_" + table_name
#%%
run_name = "'%Y%m%d-%H%M%S-run-" + my_checkpoint_name + '\''

yaml_config = f"""
name: {my_checkpoint_name}
config_version: 1.0
class_name: SimpleCheckpoint
run_name_template: {run_name}
validations:
  - batch_request:
      datasource_name: engine_sch_psql_dev
      data_connector_name: landing_tables
      data_asset_name: table_lnd_tr_proy_ano
      data_connector_query: 
        index: -1
    
    expectation_suite_name: suite_ds_tr_proy_ano
"""
print(yaml_config)
# # Customize Your Configuration
# The following cells show examples for listing your current configuration. You can replace values in the sample configuration with these values to customize your Checkpoint.

# In[13]:
# Run this cell to print out the names of your Datasources, Data Connectors and Data Assets
pprint(context.get_available_data_asset_names())
# In[14]:
# Get existing Expectations Suites
print(context.list_expectation_suite_names())

# # Test Your Checkpoint Configuration
# Here we will test your Checkpoint configuration to make sure it is valid.
#
# This `test_yaml_config()` function is meant to enable fast dev loops. If your configuration is correct, this cell will show a message that you successfully instantiated a Checkpoint. You can continually edit your Checkpoint config yaml and re-run the cell to check until the new config is valid.
#
# If you instead wish to use python instead of yaml to configure your Checkpoint, you can use `context.add_checkpoint()` and specify all the required parameters.

# In[15]:
my_checkpoint = context.test_yaml_config(yaml_config=yaml_config)
# # Review Your Checkpoint
#
# You can run the following cell to print out the full yaml configuration. For example, if you used **SimpleCheckpoint**  this will show you the default action list.

# In[17]:
print(my_checkpoint.get_config(mode="yaml"))

# # Add Your Checkpoint
#
# Run the following cell to save this Checkpoint to your Checkpoint Store.

# In[7]:
context.add_checkpoint(**yaml.load(yaml_config))

# In[18]:
# In case to need existing checkpoint uncomment de next two lines
#checkpoint = context.get_checkpoint('ckpt_tr_proy_ano')
#print(checkpoint.get_config(mode="yaml"))

# # Run Your Checkpoint & Open Data Docs(Optional)
#
# You may wish to run the Checkpoint now and review its output in Data Docs. If so uncomment and run the following cell.

# In[19]:
context.run_checkpoint(checkpoint_name=my_checkpoint_name)
context.open_data_docs()
# In[ ]:





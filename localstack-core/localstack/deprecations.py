# A simple module to track deprecations over time / versions, and some simple functions guiding the affected users.
import logging
import os
from dataclasses import dataclass
from typing import Callable, List, Optional

from localstack.utils.analytics import log

LOG = logging.getLogger(__name__)


@dataclass
class EnvVarDeprecation:
    """
    Simple class defining a deprecation of an environment variable config.
    It helps keeping track of deprecations over time.
    """

    env_var: str
    deprecation_version: str
    deprecation_path: str = None

    @property
    def is_affected(self) -> bool:
        """
        Checks whether an environment is affected.
        :return: true if the environment is affected / is using a deprecated config
        """
        return os.environ.get(self.env_var) is not None


#
# List of deprecations
#
# Please make sure this is in-sync with https://docs.localstack.cloud/references/configuration/
#
DEPRECATIONS = [
    # Since 0.11.3 - HTTP / HTTPS multiplexing
    EnvVarDeprecation(
        "USE_SSL",
        "0.11.3",
        "Each endpoint now supports multiplexing HTTP/HTTPS traffic over the same port. Please remove this environment variable.",  # noqa
    ),
    # Since 0.12.8 - PORT_UI was removed
    EnvVarDeprecation(
        "PORT_WEB_UI",
        "0.12.8",
        "PORT_WEB_UI has been removed, and is not available anymore. Please remove this environment variable.",
    ),
    # Deprecated in 0.12.7, removed in 3.0.0
    EnvVarDeprecation(
        "USE_SINGLE_REGION",
        "0.12.7",
        "LocalStack now has full multi-region support. This option has no effect. Please remove it from your configuration.",  # noqa
    ),
    # Deprecated in 0.12.7, removed in 3.0.0
    EnvVarDeprecation(
        "DEFAULT_REGION",
        "0.12.7",
        "LocalStack now has full multi-region support. This option has no effect. Please remove it from your configuration.",  # noqa
    ),
    # Since 1.0.0 - New Persistence and file system
    EnvVarDeprecation(
        "DATA_DIR",
        "1.0.0",
        "Please use PERSISTENCE instead. The state will be stored in your LocalStack volume in the state/ directory.",
    ),
    EnvVarDeprecation(
        "HOST_TMP_FOLDER",
        "1.0.0",
        "This option has no effect anymore. Please remove this environment variable.",
    ),
    EnvVarDeprecation(
        "LEGACY_DIRECTORIES",
        "1.0.0",
        "This option has no effect anymore. Please migrate to the new filesystem layout (introduced with v1.0).",
    ),
    EnvVarDeprecation(
        "TMPDIR", "1.0.0", "Please migrate to the new filesystem layout (introduced with v1.0)."
    ),
    EnvVarDeprecation(
        "PERSISTENCE_SINGLE_FILE",
        "1.0.0",
        "The legacy persistence mechanism is not supported anymore, please migrate to the advanced persistence mechanism of LocalStack Pro.",  # noqa
    ),
    # Since 1.0.0 - New ASF Gateway
    EnvVarDeprecation(
        "LEGACY_EDGE_PROXY",
        "1.0.0",
        "This option has no effect anymore. Please remove this environment variable.",
    ),
    # Since 1.1.0 - Kinesalite removed with 1.3, only kinesis-mock is used as kinesis provider / backend
    EnvVarDeprecation(
        "KINESIS_PROVIDER",
        "1.1.0",
        "This option has no effect anymore. Please remove this environment variable.",
    ),
    # Since 1.1.0 - Init dir has been deprecated in favor of pluggable init hooks
    EnvVarDeprecation(
        "LEGACY_INIT_DIR",
        "1.1.0",
        "This option has no effect anymore. "
        "Please use the pluggable initialization hooks in /etc/localhost/init/<stage>.d instead.",
    ),
    EnvVarDeprecation(
        "INIT_SCRIPTS_PATH",
        "1.1.0",
        "This option has no effect anymore. "
        "Please use the pluggable initialization hooks in /etc/localhost/init/<stage>.d instead.",
    ),
    # Since 1.3.0 - Synchronous events break AWS parity
    EnvVarDeprecation(
        "SYNCHRONOUS_SNS_EVENTS",
        "1.3.0",
        "This option has no effect anymore. Please remove this environment variable.",
    ),
    EnvVarDeprecation(
        "SYNCHRONOUS_SQS_EVENTS",
        "1.3.0",
        "This option has no effect anymore. Please remove this environment variable.",
    ),
    EnvVarDeprecation(
        "SYNCHRONOUS_API_GATEWAY_EVENTS",
        "1.3.0",
        "This option has no effect anymore. Please remove this environment variable.",
    ),
    EnvVarDeprecation(
        "SYNCHRONOUS_KINESIS_EVENTS",
        "1.3.0",
        "This option has no effect anymore. Please remove this environment variable.",
    ),
    EnvVarDeprecation(
        "SYNCHRONOUS_DYNAMODB_EVENTS",
        "1.3.0",
        "This option has no effect anymore. Please remove this environment variable.",
    ),
    # Since 1.3.0 - All non-pre-seeded infra is downloaded asynchronously
    EnvVarDeprecation(
        "SKIP_INFRA_DOWNLOADS",
        "1.3.0",
        "Infra downloads are triggered on-demand now. Please remove this environment variable.",
    ),
    # Since 1.3.0 - Mocking for unimplemented operations will be removed
    EnvVarDeprecation(
        "MOCK_UNIMPLEMENTED",
        "1.3.0",
        "This feature is not supported anymore. Please remove this environment variable.",
    ),
    # Since 1.4.0 - The Edge Forwarding is only used for legacy HTTPS proxying and will be removed
    EnvVarDeprecation(
        "EDGE_FORWARD_URL",
        "1.4.0",
        "This option has no effect anymore. Please remove this environment variable.",
    ),
    # Deprecated in 1.4.0, removed in 3.0.0
    EnvVarDeprecation(
        "KMS_PROVIDER",
        "1.4.0",
        "This option has no effect. Please remove it from your configuration.",
    ),
    # Since 2.0.0 - HOSTNAME_EXTERNAL will be replaced with LOCALSTACK_HOST
    EnvVarDeprecation(
        "HOSTNAME_EXTERNAL",
        "2.0.0",
        "This configuration will be migrated to LOCALSTACK_HOST",
    ),
    # Since 2.0.0 - LOCALSTACK_HOST will be replaced with LOCALSTACK_HOST
    EnvVarDeprecation(
        "LOCALSTACK_HOSTNAME",
        "2.0.0",
        "This configuration will be migrated to LOCALSTACK_HOST",
    ),
    # Since 2.0.0 - redefined as GATEWAY_LISTEN
    EnvVarDeprecation(
        "EDGE_BIND_HOST",
        "2.0.0",
        "This configuration will be migrated to GATEWAY_LISTEN",
    ),
    # Since 2.0.0 - redefined as GATEWAY_LISTEN
    EnvVarDeprecation(
        "EDGE_PORT",
        "2.0.0",
        "This configuration will be migrated to GATEWAY_LISTEN",
    ),
    # Since 2.0.0 - redefined as GATEWAY_LISTEN
    EnvVarDeprecation(
        "EDGE_PORT_HTTP",
        "2.0.0",
        "This configuration will be migrated to GATEWAY_LISTEN",
    ),
    EnvVarDeprecation(
        "LAMBDA_EXECUTOR",
        "2.0.0",
        "This configuration is obsolete with the new lambda provider "
        "https://docs.localstack.cloud/user-guide/aws/lambda/#migrating-to-lambda-v2\n"
        "Please mount the Docker socket /var/run/docker.sock as a volume when starting LocalStack.",
    ),
    EnvVarDeprecation(
        "LAMBDA_STAY_OPEN_MODE",
        "2.0.0",
        "Stay open mode is the default behavior in the new lambda provider "
        "https://docs.localstack.cloud/user-guide/aws/lambda/#migrating-to-lambda-v2",
    ),
    EnvVarDeprecation(
        "LAMBDA_REMOTE_DOCKER",
        "2.0.0",
        "The new lambda provider copies zip files by default and automatically configures hot reloading "
        "https://docs.localstack.cloud/user-guide/aws/lambda/#migrating-to-lambda-v2",
    ),
    EnvVarDeprecation(
        "LAMBDA_CODE_EXTRACT_TIME",
        "2.0.0",
        "Function creation now happens asynchronously in the new lambda provider "
        "https://docs.localstack.cloud/user-guide/aws/lambda/#migrating-to-lambda-v2",
    ),
    EnvVarDeprecation(
        "LAMBDA_CONTAINER_REGISTRY",
        "2.0.0",
        "The new lambda provider uses LAMBDA_RUNTIME_IMAGE_MAPPING instead "
        "https://docs.localstack.cloud/user-guide/aws/lambda/#migrating-to-lambda-v2",
    ),
    EnvVarDeprecation(
        "LAMBDA_FALLBACK_URL",
        "2.0.0",
        "This feature is not supported in the new lambda provider "
        "https://docs.localstack.cloud/user-guide/aws/lambda/#migrating-to-lambda-v2",
    ),
    EnvVarDeprecation(
        "LAMBDA_FORWARD_URL",
        "2.0.0",
        "This feature is not supported in the new lambda provider "
        "https://docs.localstack.cloud/user-guide/aws/lambda/#migrating-to-lambda-v2",
    ),
    EnvVarDeprecation(
        "LAMBDA_XRAY_INIT",
        "2.0.0",
        "The X-Ray daemon is always initialized in the new lambda provider "
        "https://docs.localstack.cloud/user-guide/aws/lambda/#migrating-to-lambda-v2",
    ),
    EnvVarDeprecation(
        "KINESIS_INITIALIZE_STREAMS",
        "1.4.0",
        "This option has no effect anymore. Please use the AWS client and init hooks instead.",
    ),
    EnvVarDeprecation(
        "SQS_PORT_EXTERNAL",
        "1.0.0",
        "This option has no effect anymore. Please use LOCALSTACK_HOST instead.",
    ),
    EnvVarDeprecation(
        "PROVIDER_OVERRIDE_LAMBDA",
        "3.0.0",
        "This option is ignored because the legacy Lambda provider (v1) has been removed since 3.0.0. "
        "Please remove PROVIDER_OVERRIDE_LAMBDA and migrate to our new Lambda provider (v2): "
        "https://docs.localstack.cloud/user-guide/aws/lambda/#migrating-to-lambda-v2",
    ),
    EnvVarDeprecation(
        "ES_CUSTOM_BACKEND",
        "0.14.0",
        "This option has no effect anymore. Please use OPENSEARCH_CUSTOM_BACKEND instead.",
    ),
    EnvVarDeprecation(
        "ES_MULTI_CLUSTER",
        "0.14.0",
        "This option has no effect anymore. Please use OPENSEARCH_MULTI_CLUSTER instead.",
    ),
    EnvVarDeprecation(
        "ES_ENDPOINT_STRATEGY",
        "0.14.0",
        "This option has no effect anymore. Please use OPENSEARCH_ENDPOINT_STRATEGY instead.",
    ),
    EnvVarDeprecation(
        "PERSIST_ALL",
        "2.3.2",
        "LocalStack treats backends and assets the same with respect to persistence. Please remove PERSIST_ALL.",
    ),
    EnvVarDeprecation(
        "DNS_LOCAL_NAME_PATTERNS",
        "3.0.0",
        "This option was confusingly named. Please use DNS_NAME_PATTERNS_TO_RESOLVE_UPSTREAM "
        "instead.",
    ),
    EnvVarDeprecation(
        "LAMBDA_EVENTS_INTERNAL_SQS",
        "4.0.0",
        "This option is ignored because the LocalStack SQS dependency for event invokes has been removed since 4.0.0"
        " in favor of a lightweight Lambda-internal SQS implementation.",
    ),
    EnvVarDeprecation(
        "LAMBDA_EVENT_SOURCE_MAPPING",
        "4.0.0",
        "This option has no effect anymore. Please remove this environment variable.",
    ),
    EnvVarDeprecation(
        "LAMBDA_SQS_EVENT_SOURCE_MAPPING_INTERVAL_SEC",
        "4.0.0",
        "This option is not supported by the new Lambda Event Source Mapping v2 implementation."
        " Please create a GitHub issue if you experience any performance challenges.",
    ),
    EnvVarDeprecation(
        "PROVIDER_OVERRIDE_STEPFUNCTIONS",
        "4.0.0",
        "This option is ignored because the legacy StepFunctions provider (v1) has been removed since 4.0.0."
        " Please remove PROVIDER_OVERRIDE_STEPFUNCTIONS.",
    ),
    EnvVarDeprecation(
        "EVENT_RULE_ENGINE",
        "4.0.3",
        "This option is ignored because the Java-based event ruler has been removed since 4.1.0."
        " Our latest Python-native implementation introduced in 4.0.3"
        " is faster, achieves great AWS parity, and fixes compatibility issues with the StepFunctions JSONata feature."
        " Please remove EVENT_RULE_ENGINE.",
    ),
    EnvVarDeprecation(
        "STEPFUNCTIONS_LAMBDA_ENDPOINT",
        "4.0.0",
        "This is only supported for the legacy provider. URL to use as the Lambda service endpoint in Step Functions. "
        "By default this is the LocalStack Lambda endpoint. Use default to select the original AWS Lambda endpoint.",
    ),
    EnvVarDeprecation(
        "LOCAL_PORT_STEPFUNCTIONS",
        "4.0.0",
        "This is only supported for the legacy provider."
        "It defines the local port to which Step Functions traffic is redirected."
        "By default, LocalStack routes Step Functions traffic to its internal runtime. "
        "Use this variable only if you need to redirect traffic to a different local Step Functions runtime.",
    ),
]


def collect_affected_deprecations(
    deprecations: Optional[List[EnvVarDeprecation]] = None,
) -> List[EnvVarDeprecation]:
    """
    Collects all deprecations which are used in the OS environ.
    :param deprecations: List of deprecations to check. Uses DEPRECATIONS list by default.
    :return: List of deprecations which are used in the current environment
    """
    if deprecations is None:
        deprecations = DEPRECATIONS
    return [deprecation for deprecation in deprecations if deprecation.is_affected]


def log_env_warning(deprecations: List[EnvVarDeprecation]) -> None:
    """
    Logs warnings for the given deprecations.
    :param deprecations: list of affected deprecations to show a warning for
    """
    """
    Logs a warning if a given environment variable is set (no matter what the value is).
    :param env_var: to check
    :param deprecation_version: version with which the env variable has been deprecated
    """
    if deprecations:
        env_vars = []

        # Print warnings for the env vars and collect them (for the analytics event)
        for deprecation in deprecations:
            LOG.warning(
                "%s is deprecated (since %s) and will be removed in upcoming releases of LocalStack! %s",
                deprecation.env_var,
                deprecation.deprecation_version,
                deprecation.deprecation_path,
            )
            env_vars.append(deprecation.env_var)

        # Log an event if deprecated env vars are used
        log.event(event="deprecated_env_usage", payload={"deprecated_env_vars": env_vars})


def log_deprecation_warnings(deprecations: Optional[List[EnvVarDeprecation]] = None) -> None:
    affected_deprecations = collect_affected_deprecations(deprecations)
    log_env_warning(affected_deprecations)

    provider_override_events = os.environ.get("PROVIDER_OVERRIDE_EVENTS")
    if provider_override_events and provider_override_events in ["v1", "legacy"]:
        env_var_value = f"PROVIDER_OVERRIDE_EVENTS={provider_override_events}"
        deprecation_version = "4.0.0"
        deprecation_path = f"Remove {env_var_value} to use the new EventBridge implementation."
        LOG.warning(
            "%s is deprecated (since %s) and will be removed in upcoming releases of LocalStack! %s",
            env_var_value,
            deprecation_version,
            deprecation_path,
        )


def deprecated_endpoint(
    endpoint: Callable, previous_path: str, deprecation_version: str, new_path: str
) -> Callable:
    """
    Wrapper function which logs a warning (and a deprecation path) whenever a deprecated URL is invoked by the router.

    :param endpoint: to wrap (log a warning whenever it is invoked)
    :param previous_path: route path it is triggered by
    :param deprecation_version: version of LocalStack with which this endpoint is deprecated
    :param new_path: new route path which should be used instead
    :return: wrapped function which can be registered for a route
    """

    def deprecated_wrapper(*args, **kwargs):
        LOG.warning(
            "%s is deprecated (since %s) and will be removed in upcoming releases of LocalStack! Use %s instead.",
            previous_path,
            deprecation_version,
            new_path,
        )
        return endpoint(*args, **kwargs)

    return deprecated_wrapper

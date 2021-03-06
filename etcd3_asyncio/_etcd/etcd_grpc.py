# Generated by the Protocol Buffers compiler. DO NOT EDIT!
# source: etcd.proto
# plugin: grpclib.plugin.main
import abc
import typing

import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server

from .gogoproto import gogo_pb2  # TODO system-wide
from . import kv_pb2
from . import auth_pb2
import google.api.annotations_pb2
from . import etcd_pb2


class KVBase(abc.ABC):

    @abc.abstractmethod
    async def Range(self, stream: 'grpclib.server.Stream[etcd_pb2.RangeRequest, etcd_pb2.RangeResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Put(self, stream: 'grpclib.server.Stream[etcd_pb2.PutRequest, etcd_pb2.PutResponse]') -> None:
        pass

    @abc.abstractmethod
    async def DeleteRange(self, stream: 'grpclib.server.Stream[etcd_pb2.DeleteRangeRequest, etcd_pb2.DeleteRangeResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Txn(self, stream: 'grpclib.server.Stream[etcd_pb2.TxnRequest, etcd_pb2.TxnResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Compact(self, stream: 'grpclib.server.Stream[etcd_pb2.CompactionRequest, etcd_pb2.CompactionResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/etcdserverpb.KV/Range': grpclib.const.Handler(
                self.Range,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.RangeRequest,
                etcd_pb2.RangeResponse,
            ),
            '/etcdserverpb.KV/Put': grpclib.const.Handler(
                self.Put,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.PutRequest,
                etcd_pb2.PutResponse,
            ),
            '/etcdserverpb.KV/DeleteRange': grpclib.const.Handler(
                self.DeleteRange,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.DeleteRangeRequest,
                etcd_pb2.DeleteRangeResponse,
            ),
            '/etcdserverpb.KV/Txn': grpclib.const.Handler(
                self.Txn,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.TxnRequest,
                etcd_pb2.TxnResponse,
            ),
            '/etcdserverpb.KV/Compact': grpclib.const.Handler(
                self.Compact,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.CompactionRequest,
                etcd_pb2.CompactionResponse,
            ),
        }


class KVStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Range = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.KV/Range',
            etcd_pb2.RangeRequest,
            etcd_pb2.RangeResponse,
        )
        self.Put = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.KV/Put',
            etcd_pb2.PutRequest,
            etcd_pb2.PutResponse,
        )
        self.DeleteRange = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.KV/DeleteRange',
            etcd_pb2.DeleteRangeRequest,
            etcd_pb2.DeleteRangeResponse,
        )
        self.Txn = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.KV/Txn',
            etcd_pb2.TxnRequest,
            etcd_pb2.TxnResponse,
        )
        self.Compact = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.KV/Compact',
            etcd_pb2.CompactionRequest,
            etcd_pb2.CompactionResponse,
        )


class WatchBase(abc.ABC):

    @abc.abstractmethod
    async def Watch(self, stream: 'grpclib.server.Stream[etcd_pb2.WatchRequest, etcd_pb2.WatchResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/etcdserverpb.Watch/Watch': grpclib.const.Handler(
                self.Watch,
                grpclib.const.Cardinality.STREAM_STREAM,
                etcd_pb2.WatchRequest,
                etcd_pb2.WatchResponse,
            ),
        }


class WatchStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Watch = grpclib.client.StreamStreamMethod(
            channel,
            '/etcdserverpb.Watch/Watch',
            etcd_pb2.WatchRequest,
            etcd_pb2.WatchResponse,
        )


class LeaseBase(abc.ABC):

    @abc.abstractmethod
    async def LeaseGrant(self, stream: 'grpclib.server.Stream[etcd_pb2.LeaseGrantRequest, etcd_pb2.LeaseGrantResponse]') -> None:
        pass

    @abc.abstractmethod
    async def LeaseRevoke(self, stream: 'grpclib.server.Stream[etcd_pb2.LeaseRevokeRequest, etcd_pb2.LeaseRevokeResponse]') -> None:
        pass

    @abc.abstractmethod
    async def LeaseKeepAlive(self, stream: 'grpclib.server.Stream[etcd_pb2.LeaseKeepAliveRequest, etcd_pb2.LeaseKeepAliveResponse]') -> None:
        pass

    @abc.abstractmethod
    async def LeaseTimeToLive(self, stream: 'grpclib.server.Stream[etcd_pb2.LeaseTimeToLiveRequest, etcd_pb2.LeaseTimeToLiveResponse]') -> None:
        pass

    @abc.abstractmethod
    async def LeaseLeases(self, stream: 'grpclib.server.Stream[etcd_pb2.LeaseLeasesRequest, etcd_pb2.LeaseLeasesResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/etcdserverpb.Lease/LeaseGrant': grpclib.const.Handler(
                self.LeaseGrant,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.LeaseGrantRequest,
                etcd_pb2.LeaseGrantResponse,
            ),
            '/etcdserverpb.Lease/LeaseRevoke': grpclib.const.Handler(
                self.LeaseRevoke,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.LeaseRevokeRequest,
                etcd_pb2.LeaseRevokeResponse,
            ),
            '/etcdserverpb.Lease/LeaseKeepAlive': grpclib.const.Handler(
                self.LeaseKeepAlive,
                grpclib.const.Cardinality.STREAM_STREAM,
                etcd_pb2.LeaseKeepAliveRequest,
                etcd_pb2.LeaseKeepAliveResponse,
            ),
            '/etcdserverpb.Lease/LeaseTimeToLive': grpclib.const.Handler(
                self.LeaseTimeToLive,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.LeaseTimeToLiveRequest,
                etcd_pb2.LeaseTimeToLiveResponse,
            ),
            '/etcdserverpb.Lease/LeaseLeases': grpclib.const.Handler(
                self.LeaseLeases,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.LeaseLeasesRequest,
                etcd_pb2.LeaseLeasesResponse,
            ),
        }


class LeaseStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.LeaseGrant = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Lease/LeaseGrant',
            etcd_pb2.LeaseGrantRequest,
            etcd_pb2.LeaseGrantResponse,
        )
        self.LeaseRevoke = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Lease/LeaseRevoke',
            etcd_pb2.LeaseRevokeRequest,
            etcd_pb2.LeaseRevokeResponse,
        )
        self.LeaseKeepAlive = grpclib.client.StreamStreamMethod(
            channel,
            '/etcdserverpb.Lease/LeaseKeepAlive',
            etcd_pb2.LeaseKeepAliveRequest,
            etcd_pb2.LeaseKeepAliveResponse,
        )
        self.LeaseTimeToLive = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Lease/LeaseTimeToLive',
            etcd_pb2.LeaseTimeToLiveRequest,
            etcd_pb2.LeaseTimeToLiveResponse,
        )
        self.LeaseLeases = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Lease/LeaseLeases',
            etcd_pb2.LeaseLeasesRequest,
            etcd_pb2.LeaseLeasesResponse,
        )


class ClusterBase(abc.ABC):

    @abc.abstractmethod
    async def MemberAdd(self, stream: 'grpclib.server.Stream[etcd_pb2.MemberAddRequest, etcd_pb2.MemberAddResponse]') -> None:
        pass

    @abc.abstractmethod
    async def MemberRemove(self, stream: 'grpclib.server.Stream[etcd_pb2.MemberRemoveRequest, etcd_pb2.MemberRemoveResponse]') -> None:
        pass

    @abc.abstractmethod
    async def MemberUpdate(self, stream: 'grpclib.server.Stream[etcd_pb2.MemberUpdateRequest, etcd_pb2.MemberUpdateResponse]') -> None:
        pass

    @abc.abstractmethod
    async def MemberList(self, stream: 'grpclib.server.Stream[etcd_pb2.MemberListRequest, etcd_pb2.MemberListResponse]') -> None:
        pass

    @abc.abstractmethod
    async def MemberPromote(self, stream: 'grpclib.server.Stream[etcd_pb2.MemberPromoteRequest, etcd_pb2.MemberPromoteResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/etcdserverpb.Cluster/MemberAdd': grpclib.const.Handler(
                self.MemberAdd,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.MemberAddRequest,
                etcd_pb2.MemberAddResponse,
            ),
            '/etcdserverpb.Cluster/MemberRemove': grpclib.const.Handler(
                self.MemberRemove,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.MemberRemoveRequest,
                etcd_pb2.MemberRemoveResponse,
            ),
            '/etcdserverpb.Cluster/MemberUpdate': grpclib.const.Handler(
                self.MemberUpdate,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.MemberUpdateRequest,
                etcd_pb2.MemberUpdateResponse,
            ),
            '/etcdserverpb.Cluster/MemberList': grpclib.const.Handler(
                self.MemberList,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.MemberListRequest,
                etcd_pb2.MemberListResponse,
            ),
            '/etcdserverpb.Cluster/MemberPromote': grpclib.const.Handler(
                self.MemberPromote,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.MemberPromoteRequest,
                etcd_pb2.MemberPromoteResponse,
            ),
        }


class ClusterStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.MemberAdd = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Cluster/MemberAdd',
            etcd_pb2.MemberAddRequest,
            etcd_pb2.MemberAddResponse,
        )
        self.MemberRemove = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Cluster/MemberRemove',
            etcd_pb2.MemberRemoveRequest,
            etcd_pb2.MemberRemoveResponse,
        )
        self.MemberUpdate = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Cluster/MemberUpdate',
            etcd_pb2.MemberUpdateRequest,
            etcd_pb2.MemberUpdateResponse,
        )
        self.MemberList = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Cluster/MemberList',
            etcd_pb2.MemberListRequest,
            etcd_pb2.MemberListResponse,
        )
        self.MemberPromote = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Cluster/MemberPromote',
            etcd_pb2.MemberPromoteRequest,
            etcd_pb2.MemberPromoteResponse,
        )


class MaintenanceBase(abc.ABC):

    @abc.abstractmethod
    async def Alarm(self, stream: 'grpclib.server.Stream[etcd_pb2.AlarmRequest, etcd_pb2.AlarmResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Status(self, stream: 'grpclib.server.Stream[etcd_pb2.StatusRequest, etcd_pb2.StatusResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Defragment(self, stream: 'grpclib.server.Stream[etcd_pb2.DefragmentRequest, etcd_pb2.DefragmentResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Hash(self, stream: 'grpclib.server.Stream[etcd_pb2.HashRequest, etcd_pb2.HashResponse]') -> None:
        pass

    @abc.abstractmethod
    async def HashKV(self, stream: 'grpclib.server.Stream[etcd_pb2.HashKVRequest, etcd_pb2.HashKVResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Snapshot(self, stream: 'grpclib.server.Stream[etcd_pb2.SnapshotRequest, etcd_pb2.SnapshotResponse]') -> None:
        pass

    @abc.abstractmethod
    async def MoveLeader(self, stream: 'grpclib.server.Stream[etcd_pb2.MoveLeaderRequest, etcd_pb2.MoveLeaderResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Downgrade(self, stream: 'grpclib.server.Stream[etcd_pb2.DowngradeRequest, etcd_pb2.DowngradeResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/etcdserverpb.Maintenance/Alarm': grpclib.const.Handler(
                self.Alarm,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AlarmRequest,
                etcd_pb2.AlarmResponse,
            ),
            '/etcdserverpb.Maintenance/Status': grpclib.const.Handler(
                self.Status,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.StatusRequest,
                etcd_pb2.StatusResponse,
            ),
            '/etcdserverpb.Maintenance/Defragment': grpclib.const.Handler(
                self.Defragment,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.DefragmentRequest,
                etcd_pb2.DefragmentResponse,
            ),
            '/etcdserverpb.Maintenance/Hash': grpclib.const.Handler(
                self.Hash,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.HashRequest,
                etcd_pb2.HashResponse,
            ),
            '/etcdserverpb.Maintenance/HashKV': grpclib.const.Handler(
                self.HashKV,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.HashKVRequest,
                etcd_pb2.HashKVResponse,
            ),
            '/etcdserverpb.Maintenance/Snapshot': grpclib.const.Handler(
                self.Snapshot,
                grpclib.const.Cardinality.UNARY_STREAM,
                etcd_pb2.SnapshotRequest,
                etcd_pb2.SnapshotResponse,
            ),
            '/etcdserverpb.Maintenance/MoveLeader': grpclib.const.Handler(
                self.MoveLeader,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.MoveLeaderRequest,
                etcd_pb2.MoveLeaderResponse,
            ),
            '/etcdserverpb.Maintenance/Downgrade': grpclib.const.Handler(
                self.Downgrade,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.DowngradeRequest,
                etcd_pb2.DowngradeResponse,
            ),
        }


class MaintenanceStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Alarm = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Maintenance/Alarm',
            etcd_pb2.AlarmRequest,
            etcd_pb2.AlarmResponse,
        )
        self.Status = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Maintenance/Status',
            etcd_pb2.StatusRequest,
            etcd_pb2.StatusResponse,
        )
        self.Defragment = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Maintenance/Defragment',
            etcd_pb2.DefragmentRequest,
            etcd_pb2.DefragmentResponse,
        )
        self.Hash = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Maintenance/Hash',
            etcd_pb2.HashRequest,
            etcd_pb2.HashResponse,
        )
        self.HashKV = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Maintenance/HashKV',
            etcd_pb2.HashKVRequest,
            etcd_pb2.HashKVResponse,
        )
        self.Snapshot = grpclib.client.UnaryStreamMethod(
            channel,
            '/etcdserverpb.Maintenance/Snapshot',
            etcd_pb2.SnapshotRequest,
            etcd_pb2.SnapshotResponse,
        )
        self.MoveLeader = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Maintenance/MoveLeader',
            etcd_pb2.MoveLeaderRequest,
            etcd_pb2.MoveLeaderResponse,
        )
        self.Downgrade = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Maintenance/Downgrade',
            etcd_pb2.DowngradeRequest,
            etcd_pb2.DowngradeResponse,
        )


class AuthBase(abc.ABC):

    @abc.abstractmethod
    async def AuthEnable(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthEnableRequest, etcd_pb2.AuthEnableResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AuthDisable(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthDisableRequest, etcd_pb2.AuthDisableResponse]') -> None:
        pass

    @abc.abstractmethod
    async def AuthStatus(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthStatusRequest, etcd_pb2.AuthStatusResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Authenticate(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthenticateRequest, etcd_pb2.AuthenticateResponse]') -> None:
        pass

    @abc.abstractmethod
    async def UserAdd(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthUserAddRequest, etcd_pb2.AuthUserAddResponse]') -> None:
        pass

    @abc.abstractmethod
    async def UserGet(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthUserGetRequest, etcd_pb2.AuthUserGetResponse]') -> None:
        pass

    @abc.abstractmethod
    async def UserList(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthUserListRequest, etcd_pb2.AuthUserListResponse]') -> None:
        pass

    @abc.abstractmethod
    async def UserDelete(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthUserDeleteRequest, etcd_pb2.AuthUserDeleteResponse]') -> None:
        pass

    @abc.abstractmethod
    async def UserChangePassword(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthUserChangePasswordRequest, etcd_pb2.AuthUserChangePasswordResponse]') -> None:
        pass

    @abc.abstractmethod
    async def UserGrantRole(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthUserGrantRoleRequest, etcd_pb2.AuthUserGrantRoleResponse]') -> None:
        pass

    @abc.abstractmethod
    async def UserRevokeRole(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthUserRevokeRoleRequest, etcd_pb2.AuthUserRevokeRoleResponse]') -> None:
        pass

    @abc.abstractmethod
    async def RoleAdd(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthRoleAddRequest, etcd_pb2.AuthRoleAddResponse]') -> None:
        pass

    @abc.abstractmethod
    async def RoleGet(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthRoleGetRequest, etcd_pb2.AuthRoleGetResponse]') -> None:
        pass

    @abc.abstractmethod
    async def RoleList(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthRoleListRequest, etcd_pb2.AuthRoleListResponse]') -> None:
        pass

    @abc.abstractmethod
    async def RoleDelete(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthRoleDeleteRequest, etcd_pb2.AuthRoleDeleteResponse]') -> None:
        pass

    @abc.abstractmethod
    async def RoleGrantPermission(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthRoleGrantPermissionRequest, etcd_pb2.AuthRoleGrantPermissionResponse]') -> None:
        pass

    @abc.abstractmethod
    async def RoleRevokePermission(self, stream: 'grpclib.server.Stream[etcd_pb2.AuthRoleRevokePermissionRequest, etcd_pb2.AuthRoleRevokePermissionResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/etcdserverpb.Auth/AuthEnable': grpclib.const.Handler(
                self.AuthEnable,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthEnableRequest,
                etcd_pb2.AuthEnableResponse,
            ),
            '/etcdserverpb.Auth/AuthDisable': grpclib.const.Handler(
                self.AuthDisable,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthDisableRequest,
                etcd_pb2.AuthDisableResponse,
            ),
            '/etcdserverpb.Auth/AuthStatus': grpclib.const.Handler(
                self.AuthStatus,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthStatusRequest,
                etcd_pb2.AuthStatusResponse,
            ),
            '/etcdserverpb.Auth/Authenticate': grpclib.const.Handler(
                self.Authenticate,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthenticateRequest,
                etcd_pb2.AuthenticateResponse,
            ),
            '/etcdserverpb.Auth/UserAdd': grpclib.const.Handler(
                self.UserAdd,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthUserAddRequest,
                etcd_pb2.AuthUserAddResponse,
            ),
            '/etcdserverpb.Auth/UserGet': grpclib.const.Handler(
                self.UserGet,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthUserGetRequest,
                etcd_pb2.AuthUserGetResponse,
            ),
            '/etcdserverpb.Auth/UserList': grpclib.const.Handler(
                self.UserList,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthUserListRequest,
                etcd_pb2.AuthUserListResponse,
            ),
            '/etcdserverpb.Auth/UserDelete': grpclib.const.Handler(
                self.UserDelete,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthUserDeleteRequest,
                etcd_pb2.AuthUserDeleteResponse,
            ),
            '/etcdserverpb.Auth/UserChangePassword': grpclib.const.Handler(
                self.UserChangePassword,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthUserChangePasswordRequest,
                etcd_pb2.AuthUserChangePasswordResponse,
            ),
            '/etcdserverpb.Auth/UserGrantRole': grpclib.const.Handler(
                self.UserGrantRole,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthUserGrantRoleRequest,
                etcd_pb2.AuthUserGrantRoleResponse,
            ),
            '/etcdserverpb.Auth/UserRevokeRole': grpclib.const.Handler(
                self.UserRevokeRole,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthUserRevokeRoleRequest,
                etcd_pb2.AuthUserRevokeRoleResponse,
            ),
            '/etcdserverpb.Auth/RoleAdd': grpclib.const.Handler(
                self.RoleAdd,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthRoleAddRequest,
                etcd_pb2.AuthRoleAddResponse,
            ),
            '/etcdserverpb.Auth/RoleGet': grpclib.const.Handler(
                self.RoleGet,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthRoleGetRequest,
                etcd_pb2.AuthRoleGetResponse,
            ),
            '/etcdserverpb.Auth/RoleList': grpclib.const.Handler(
                self.RoleList,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthRoleListRequest,
                etcd_pb2.AuthRoleListResponse,
            ),
            '/etcdserverpb.Auth/RoleDelete': grpclib.const.Handler(
                self.RoleDelete,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthRoleDeleteRequest,
                etcd_pb2.AuthRoleDeleteResponse,
            ),
            '/etcdserverpb.Auth/RoleGrantPermission': grpclib.const.Handler(
                self.RoleGrantPermission,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthRoleGrantPermissionRequest,
                etcd_pb2.AuthRoleGrantPermissionResponse,
            ),
            '/etcdserverpb.Auth/RoleRevokePermission': grpclib.const.Handler(
                self.RoleRevokePermission,
                grpclib.const.Cardinality.UNARY_UNARY,
                etcd_pb2.AuthRoleRevokePermissionRequest,
                etcd_pb2.AuthRoleRevokePermissionResponse,
            ),
        }


class AuthStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.AuthEnable = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/AuthEnable',
            etcd_pb2.AuthEnableRequest,
            etcd_pb2.AuthEnableResponse,
        )
        self.AuthDisable = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/AuthDisable',
            etcd_pb2.AuthDisableRequest,
            etcd_pb2.AuthDisableResponse,
        )
        self.AuthStatus = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/AuthStatus',
            etcd_pb2.AuthStatusRequest,
            etcd_pb2.AuthStatusResponse,
        )
        self.Authenticate = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/Authenticate',
            etcd_pb2.AuthenticateRequest,
            etcd_pb2.AuthenticateResponse,
        )
        self.UserAdd = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/UserAdd',
            etcd_pb2.AuthUserAddRequest,
            etcd_pb2.AuthUserAddResponse,
        )
        self.UserGet = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/UserGet',
            etcd_pb2.AuthUserGetRequest,
            etcd_pb2.AuthUserGetResponse,
        )
        self.UserList = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/UserList',
            etcd_pb2.AuthUserListRequest,
            etcd_pb2.AuthUserListResponse,
        )
        self.UserDelete = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/UserDelete',
            etcd_pb2.AuthUserDeleteRequest,
            etcd_pb2.AuthUserDeleteResponse,
        )
        self.UserChangePassword = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/UserChangePassword',
            etcd_pb2.AuthUserChangePasswordRequest,
            etcd_pb2.AuthUserChangePasswordResponse,
        )
        self.UserGrantRole = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/UserGrantRole',
            etcd_pb2.AuthUserGrantRoleRequest,
            etcd_pb2.AuthUserGrantRoleResponse,
        )
        self.UserRevokeRole = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/UserRevokeRole',
            etcd_pb2.AuthUserRevokeRoleRequest,
            etcd_pb2.AuthUserRevokeRoleResponse,
        )
        self.RoleAdd = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/RoleAdd',
            etcd_pb2.AuthRoleAddRequest,
            etcd_pb2.AuthRoleAddResponse,
        )
        self.RoleGet = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/RoleGet',
            etcd_pb2.AuthRoleGetRequest,
            etcd_pb2.AuthRoleGetResponse,
        )
        self.RoleList = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/RoleList',
            etcd_pb2.AuthRoleListRequest,
            etcd_pb2.AuthRoleListResponse,
        )
        self.RoleDelete = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/RoleDelete',
            etcd_pb2.AuthRoleDeleteRequest,
            etcd_pb2.AuthRoleDeleteResponse,
        )
        self.RoleGrantPermission = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/RoleGrantPermission',
            etcd_pb2.AuthRoleGrantPermissionRequest,
            etcd_pb2.AuthRoleGrantPermissionResponse,
        )
        self.RoleRevokePermission = grpclib.client.UnaryUnaryMethod(
            channel,
            '/etcdserverpb.Auth/RoleRevokePermission',
            etcd_pb2.AuthRoleRevokePermissionRequest,
            etcd_pb2.AuthRoleRevokePermissionResponse,
        )

from cosm.query.rest_client import RestClient

from cosmos.bank.v1beta1.query_pb2 import *
from google.protobuf.json_format import Parse


class BankRest:
    def __init__(self, rest_address: str):
        self.rest_api = RestClient(rest_address)

    def Balance(self, request: QueryBalanceRequest) -> QueryBalanceResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/balances/{request.address}/{request.denom}")
        return Parse(json_response, QueryBalanceResponse())

    def AllBalances(self, request: QueryAllBalancesRequest) -> QueryAllBalancesResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/balances/{request.address}")
        return Parse(json_response, QueryAllBalancesResponse())

    def TotalSupply(self) -> QueryTotalSupplyResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/supply")
        return Parse(json_response, QueryTotalSupplyResponse())

    def SupplyOf(self, request: QuerySupplyOfRequest) -> QuerySupplyOfResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/supply/{request.denom}")
        return Parse(json_response, QuerySupplyOfResponse())

    def Params(self, request: QueryParamsRequest) -> QueryParamsResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/params")
        return Parse(json_response, QueryParamsResponse())

    def DenomMetadata(self, request: QueryDenomMetadataRequest) -> QueryDenomMetadataResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/denoms_metadata/{request.denom}")
        return Parse(json_response, QueryDenomMetadataResponse())

    def DenomsMetadata(self, request: QueryDenomsMetadataRequest) -> QueryDenomsMetadataResponse:
        json_response = self.rest_api.query(f"/cosmos/bank/v1beta1/denoms_metadata")
        return Parse(json_response, QueryDenomsMetadataResponse())

# # ⚠ Warning
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# [🥭 Mango Markets](https://mango.markets/) support is available at:
#   [Docs](https://docs.mango.markets/)
#   [Discord](https://discord.gg/67jySBhxrg)
#   [Twitter](https://twitter.com/mangomarkets)
#   [Github](https://github.com/blockworks-foundation)
#   [Email](mailto:hello@blockworks.foundation)


import typing

from .account import Account
from .context import Context
from .group import Group
from .market import Market
from .marketoperations import MarketOperations, NullMarketOperations
from .perpmarket import PerpMarket
from .perpmarketoperations import PerpMarketOperations
# from .serummarketoperations import SerumMarketOperations
from .spotmarket import SpotMarket
from .wallet import Wallet

# # 🥭 create_market_operations
#
# This function deals with the creation of a `MarketOperations` object for a given `Market`.


def create_market_operations(context: Context, wallet: Wallet, dry_run: bool, market: Market, reporter: typing.Callable[[str], None]) -> MarketOperations:
    if dry_run:
        return NullMarketOperations(market.symbol, reporter)
    elif isinstance(market, SpotMarket):
        #     return SerumMarketOperations(context, wallet, market, reporter)
        # elif isinstance(market, PerpMarket):
        group = Group.load(context, context.group_id)
        margin_accounts = Account.load_all_for_owner(context, wallet.address, group)
        perp_market_info = group.perp_markets[0]
        if perp_market_info is None:
            raise Exception("Perp market not found at index 0.")
        perp_market = PerpMarket.load(context, group, perp_market_info.address)
        return PerpMarketOperations(market.symbol, context, wallet, margin_accounts[0], perp_market, reporter)
    else:
        raise Exception(f"Could not find order placer for market {market.symbol}")

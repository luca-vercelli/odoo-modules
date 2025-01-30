# -*- coding: utf-8 -*-
##############################################################################
#
#    Luca Vercelli 2016. Released under GNU Affero General Public License.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################



{
    'name': 'Send Invoices to Sistema TS',
    'version': '16.0.4.0.0',
    'category': 'Localization/Italy',
    'author': 'Luca Vercelli',
    'website': 'https://github.com/luca-vercelli/odoo-modules',
    'depends': ['base','account','l10n_it_fiscalcode'],
    'data': [
        'security/ir.model.access.csv',
        'views/invoice_report.xml',
        'views/product_view.xml',
        'views/partner_view.xml',
        'views/runs_view.xml',
        'views/res_config_view.xml',
        'views/wizards_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
	'license' : 'AGPL-3',
    'external_dependencies': {
        'python': ['Crypto', 'zeep', 'requests'],  #pip install pycrypthodome zeep requests
    }
}

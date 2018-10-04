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
    'version': '1.2',
    'category': 'Accounting',
    'description': """
Export a number of invoices in a XML format suitable for Italian 'Sistema Tessera Sanitaria (TS)'.

QUESTO MODULO E' RIMOSSO PERCHE' ANCORA IN BETA
""",
    'author': 'Luca Vercelli',
    'depends': ['base','account','l10n_it_fiscalcode'],
    'data': [
        'views/invoice_report.xml',
        'views/product_view.xml',
        'views/partner_view.xml',
        'views/runs_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'app': True,
}
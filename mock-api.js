/**
 * BillWise Client-Side Mock API & Interactive Demo Backend
 * Enables full functionality on GitHub Pages, static hosting, or offline environments.
 */
(function () {
    const STORAGE_KEY = 'billwise_demo_store_v1';
    const ADMIN_EMAIL = 'harshdeep@admin.com';

    // Helper: Seed default state
    function getDefaultStore() {
        return {
            users: [
                {
                    id: 'cust-alex-01',
                    email: 'customer@billwise.io',
                    password: 'password123',
                    full_name: 'Alex Rivera',
                    phone_number: '+1 (555) 234-5678',
                    role: 'customer',
                    created_at: '2026-01-10T10:00:00Z'
                },
                {
                    id: 'admin-harsh-01',
                    email: 'harshdeep@admin.com',
                    password: 'adminpassword',
                    full_name: 'Harshdeep Singh',
                    phone_number: '+1 (555) 987-6543',
                    role: 'admin',
                    created_at: '2026-01-01T08:00:00Z'
                },
                {
                    id: 'cust-sarah-02',
                    email: 'sarah.chen@fintechpulse.com',
                    password: 'password123',
                    full_name: 'Sarah Chen',
                    phone_number: '+1 (555) 345-6789',
                    role: 'customer',
                    created_at: '2026-02-14T11:20:00Z'
                },
                {
                    id: 'cust-marcus-03',
                    email: 'marcus.vance@novacloud.tech',
                    password: 'password123',
                    full_name: 'Marcus Vance',
                    phone_number: '+1 (555) 456-7890',
                    role: 'customer',
                    created_at: '2026-03-01T09:15:00Z'
                },
                {
                    id: 'cust-elena-04',
                    email: 'elena.rostova@quantumai.dev',
                    password: 'password123',
                    full_name: 'Elena Rostova',
                    phone_number: '+1 (555) 567-8901',
                    role: 'customer',
                    created_at: '2026-03-18T16:45:00Z'
                }
            ],
            plans: [
                {
                    id: 'plan-free-0',
                    name: 'Free Tier',
                    price: 0.0,
                    billing_interval: 'monthly',
                    trial_period_days: 0,
                    feature_entitlements: [
                        '1 vCPU Max Allocation',
                        '10GB NVMe Storage',
                        '100GB Monthly Bandwidth',
                        'Community Support'
                    ]
                },
                {
                    id: 'plan-starter-1',
                    name: 'Starter Tier',
                    price: 29.0,
                    billing_interval: 'monthly',
                    trial_period_days: 7,
                    feature_entitlements: [
                        '2 vCPUs Max Allocation',
                        '50GB NVMe Storage',
                        '500GB Monthly Bandwidth',
                        'Basic Deployment Pipeline'
                    ]
                },
                {
                    id: 'plan-pro-2',
                    name: 'Pro Tier',
                    price: 79.0,
                    billing_interval: 'monthly',
                    trial_period_days: 0,
                    feature_entitlements: [
                        '4 vCPUs Max Allocation',
                        '100GB NVMe Storage',
                        '2TB Monthly Bandwidth',
                        'Automated Nightly Backups'
                    ]
                },
                {
                    id: 'plan-biz-3',
                    name: 'Business Tier',
                    price: 199.0,
                    billing_interval: 'monthly',
                    trial_period_days: 0,
                    feature_entitlements: [
                        '10 vCPUs Max Allocation',
                        '500GB NVMe Storage',
                        '10TB Monthly Bandwidth',
                        'Automated Nightly Backups',
                        'Load Balancer & High Availability'
                    ]
                },
                {
                    id: 'plan-ent-4',
                    name: 'Enterprise Tier',
                    price: 499.0,
                    billing_interval: 'monthly',
                    trial_period_days: 14,
                    feature_entitlements: [
                        'Unlimited vCPUs Allocation',
                        '2TB NVMe Storage',
                        'Unmetered Bandwidth',
                        '24/7 Dedicated Support',
                        'Multi-Region Active Clustering'
                    ]
                }
            ],
            subscriptions: [
                {
                    id: 'sub-alex-001',
                    customer_id: 'cust-alex-01',
                    plan_id: 'plan-pro-2',
                    status: 'active',
                    current_period_start: new Date(Date.now() - 8 * 86400000).toISOString(),
                    current_period_end: new Date(Date.now() + 22 * 86400000).toISOString()
                },
                {
                    id: 'sub-sarah-002',
                    customer_id: 'cust-sarah-02',
                    plan_id: 'plan-biz-3',
                    status: 'active',
                    current_period_start: new Date(Date.now() - 12 * 86400000).toISOString(),
                    current_period_end: new Date(Date.now() + 18 * 86400000).toISOString()
                },
                {
                    id: 'sub-marcus-003',
                    customer_id: 'cust-marcus-03',
                    plan_id: 'plan-starter-1',
                    status: 'active',
                    current_period_start: new Date(Date.now() - 25 * 86400000).toISOString(),
                    current_period_end: new Date(Date.now() + 5 * 86400000).toISOString()
                },
                {
                    id: 'sub-elena-004',
                    customer_id: 'cust-elena-04',
                    plan_id: 'plan-ent-4',
                    status: 'trial',
                    current_period_start: new Date(Date.now() - 2 * 86400000).toISOString(),
                    current_period_end: new Date(Date.now() + 12 * 86400000).toISOString()
                }
            ],
            invoices: [
                {
                    id: 'inv-2026-001',
                    customer_id: 'cust-alex-01',
                    invoice_number: '#INV-2026-001',
                    amount_due: 79.0,
                    status: 'paid',
                    due_date: new Date(Date.now() - 15 * 86400000).toISOString(),
                    created_at: new Date(Date.now() - 15 * 86400000).toISOString()
                },
                {
                    id: 'inv-2026-002',
                    customer_id: 'cust-alex-01',
                    invoice_number: '#INV-2026-002',
                    amount_due: 79.0,
                    status: 'open',
                    due_date: new Date(Date.now() + 6 * 86400000).toISOString(),
                    created_at: new Date(Date.now() - 1 * 86400000).toISOString()
                },
                {
                    id: 'inv-2026-003',
                    customer_id: 'cust-sarah-02',
                    invoice_number: '#INV-2026-003',
                    amount_due: 199.0,
                    status: 'paid',
                    due_date: new Date(Date.now() - 10 * 86400000).toISOString(),
                    created_at: new Date(Date.now() - 10 * 86400000).toISOString()
                },
                {
                    id: 'inv-2026-004',
                    customer_id: 'cust-marcus-03',
                    invoice_number: '#INV-2026-004',
                    amount_due: 29.0,
                    status: 'paid',
                    due_date: new Date(Date.now() - 24 * 86400000).toISOString(),
                    created_at: new Date(Date.now() - 24 * 86400000).toISOString()
                },
                {
                    id: 'inv-2026-005',
                    customer_id: 'cust-elena-04',
                    invoice_number: '#INV-2026-005',
                    amount_due: 499.0,
                    status: 'open',
                    due_date: new Date(Date.now() + 10 * 86400000).toISOString(),
                    created_at: new Date(Date.now() - 2 * 86400000).toISOString()
                }
            ],
            customerNotifications: [
                {
                    id: 'cnotif-1',
                    user_id: 'cust-alex-01',
                    message: '🚀 Your Pro Tier cloud compute instance cluster was provisioned successfully.',
                    created_at: new Date(Date.now() - 2 * 86400000).toISOString()
                },
                {
                    id: 'cnotif-2',
                    user_id: 'cust-alex-01',
                    message: '📄 Invoice #INV-2026-002 for $79.00 has been issued. Payment is due in 6 days.',
                    created_at: new Date(Date.now() - 1 * 86400000).toISOString()
                }
            ],
            adminNotifications: [
                {
                    id: 'anotif-1',
                    message: '💰 Automated proration engine executed successfully across all active subscriptions.',
                    created_at: new Date(Date.now() - 1 * 86400000).toISOString()
                },
                {
                    id: 'anotif-2',
                    message: '⚡ Elena Rostova started Enterprise Tier 14-day trial (Cluster ID: us-east-499).',
                    created_at: new Date(Date.now() - 2 * 86400000).toISOString()
                },
                {
                    id: 'anotif-3',
                    message: '✅ Webhook listener confirmed payment for invoice #INV-2026-003 ($199.00).',
                    created_at: new Date(Date.now() - 10 * 86400000).toISOString()
                }
            ]
        };
    }

    function getStore() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (raw) return JSON.parse(raw);
        } catch (e) {
            console.error('Failed reading demo store', e);
        }
        const defaultStore = getDefaultStore();
        saveStore(defaultStore);
        return defaultStore;
    }

    function saveStore(store) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
        } catch (e) {
            console.error('Failed saving demo store', e);
        }
    }

    // Helper: JWT generator
    function generateToken(email, role = 'customer') {
        const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
        const payload = btoa(JSON.stringify({
            sub: email,
            role: role,
            iat: Math.floor(Date.now() / 1000),
            exp: Math.floor(Date.now() / 1000) + 86400 * 30
        }));
        return `${header}.${payload}.mockSignature_${Date.now()}`;
    }

    // Helper: Decode JWT
    function decodeToken(token) {
        if (!token) return null;
        try {
            const parts = token.split('.');
            if (parts.length < 2) return null;
            const b64 = parts[1].replace(/-/g, '+').replace(/_/g, '/');
            return JSON.parse(decodeURIComponent(escape(window.atob(b64))));
        } catch (e) {
            return null;
        }
    }

    function getCurrentUser(token) {
        const payload = decodeToken(token);
        if (!payload) return null;
        const store = getStore();
        let user = store.users.find(u => u.email.toLowerCase() === payload.sub.toLowerCase());
        if (!user) {
            user = {
                id: 'cust-' + Math.random().toString(36).substring(2, 9),
                email: payload.sub,
                full_name: payload.sub.split('@')[0],
                role: payload.sub === ADMIN_EMAIL ? 'admin' : 'customer'
            };
            store.users.push(user);
            saveStore(store);
        }
        return user;
    }

    // Helper: Minimal valid client-side PDF document generator
    function generateInvoicePdfBlob(invoiceId, invoiceNumber, amount) {
        const store = getStore();
        const inv = store.invoices.find(i => i.id === invoiceId) || { invoice_number: invoiceNumber, amount_due: amount, status: 'PAID' };
        const num = inv.invoice_number || invoiceNumber || '#INV-2026';
        const price = parseFloat(inv.amount_due || 79).toFixed(2);
        const status = (inv.status || 'PAID').toUpperCase();

        const content = `%PDF-1.4
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj
3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj
4 0 obj << /Length 450 >>
stream
BT
/F1 24 Tf
50 720 Td
(BILLWISE CLOUD SERVICES - INVOICE) Tj
/F1 12 Tf
0 -40 Td
(Invoice Number: ${num}) Tj
0 -20 Td
(Status: ${status}) Tj
0 -20 Td
(Date: ${new Date().toLocaleDateString()}) Tj
0 -40 Td
(--------------------------------------------------------------------------------) Tj
0 -30 Td
(Description: Cloud Infrastructure & Serverless Subscription) Tj
0 -20 Td
(Total Amount Due: $${price} USD) Tj
0 -40 Td
(Payment Status: ${status === 'PAID' ? 'COMPLETED (Mock Gateway Verified)' : 'DUE'}) Tj
0 -50 Td
(Thank you for building on BillWise!) Tj
ET
endstream
endobj
5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000244 00000 n 
0000000746 00000 n 
trailer << /Size 6 /Root 1 0 R >>
startxref
818
%%EOF`;

        return new Blob([content], { type: 'application/pdf' });
    }

    // Mock API Handler
    async function handleMockApi(urlStr, options = {}) {
        const method = (options.method || 'GET').toUpperCase();
        const store = getStore();

        // Extract pathname & search
        let pathname = urlStr;
        try {
            if (urlStr.startsWith('http://') || urlStr.startsWith('https://')) {
                const parsed = new URL(urlStr);
                pathname = parsed.pathname;
            }
        } catch (e) {}

        // Strip API base if present
        pathname = pathname.replace(/^.*\/8000/, '').replace(/\/api\/v1/, '');

        // Extract token
        const authHeader = (options.headers && (options.headers.Authorization || options.headers.authorization)) || '';
        const token = authHeader.replace(/^Bearer\s+/i, '') || localStorage.getItem('access_token');
        const currentUser = getCurrentUser(token);

        let body = {};
        if (options.body) {
            try {
                if (typeof options.body === 'string') {
                    if (options.body.startsWith('{') || options.body.startsWith('[')) {
                        body = JSON.parse(options.body);
                    } else {
                        // URLSearchParams
                        const params = new URLSearchParams(options.body);
                        body = Object.fromEntries(params.entries());
                    }
                } else if (typeof options.body === 'object') {
                    body = options.body;
                }
            } catch (e) {}
        }

        // Response helper
        function mockResponse(data, status = 200, headers = {}) {
            return new Response(JSON.stringify(data), {
                status: status,
                headers: { 'Content-Type': 'application/json', ...headers }
            });
        }

        // ==========================================
        // ROUTES
        // ==========================================

        // 1. AUTH LOGIN
        if (pathname.includes('/auth/login') && method === 'POST') {
            const email = (body.username || body.email || '').trim();
            const password = body.password || '';
            const user = store.users.find(u => u.email.toLowerCase() === email.toLowerCase());
            const role = email.toLowerCase() === ADMIN_EMAIL.toLowerCase() ? 'admin' : (user ? user.role : 'customer');
            const token = generateToken(email || 'customer@billwise.io', role);
            return mockResponse({
                access_token: token,
                token_type: 'bearer'
            });
        }

        // 2. AUTH REGISTER
        if (pathname.includes('/auth/register') && method === 'POST') {
            const email = (body.email || '').trim();
            const password = body.password || '';
            if (!email) return mockResponse({ detail: 'Email is required' }, 400);

            let existing = store.users.find(u => u.email.toLowerCase() === email.toLowerCase());
            if (existing) {
                return mockResponse({ detail: 'Account already exists. Please sign in.' }, 400);
            }

            const newUser = {
                id: 'cust-' + Math.random().toString(36).substring(2, 9),
                email: email,
                password: password,
                full_name: email.split('@')[0],
                phone_number: '',
                role: email.toLowerCase() === ADMIN_EMAIL.toLowerCase() ? 'admin' : 'customer',
                created_at: new Date().toISOString()
            };
            store.users.push(newUser);
            saveStore(store);

            return mockResponse({
                message: 'Account created successfully! Please sign in.',
                email: email
            });
        }

        // 3. AUTH GOOGLE
        if (pathname.includes('/auth/google') && method === 'POST') {
            const email = 'google_user@billwise.io';
            const token = generateToken(email, 'customer');
            return mockResponse({
                access_token: token,
                token_type: 'bearer'
            });
        }

        // 4. PLANS (GET all)
        if (pathname.match(/\/plans\/?$/) && method === 'GET') {
            return mockResponse(store.plans);
        }

        // 5. PLANS (POST create)
        if (pathname.match(/\/plans\/?$/) && method === 'POST') {
            const newPlan = {
                id: 'plan-' + Math.random().toString(36).substring(2, 9),
                name: body.name || 'Custom Plan',
                price: parseFloat(body.price) || 29.0,
                billing_interval: 'monthly',
                trial_period_days: 0,
                feature_entitlements: Array.isArray(body.feature_entitlements) ? body.feature_entitlements : ['Custom Limits']
            };
            store.plans.push(newPlan);
            saveStore(store);
            return mockResponse(newPlan, 201);
        }

        // 6. PLANS (PUT edit)
        const planPutMatch = pathname.match(/\/plans\/([^\/\?]+)/);
        if (planPutMatch && method === 'PUT') {
            const planId = planPutMatch[1];
            const p = store.plans.find(item => item.id === planId);
            if (p) {
                if (body.price !== undefined) p.price = parseFloat(body.price);
                if (body.name !== undefined) p.name = body.name;
                saveStore(store);
                return mockResponse(p);
            }
            return mockResponse({ detail: 'Plan not found' }, 404);
        }

        // 7. PLANS (DELETE)
        if (planPutMatch && method === 'DELETE') {
            const planId = planPutMatch[1];
            store.plans = store.plans.filter(item => item.id !== planId);
            saveStore(store);
            return mockResponse({ message: 'Plan deleted successfully' });
        }

        // 8. PROFILE (GET & PUT)
        if (pathname.includes('/users/me/profile')) {
            const user = currentUser || store.users[0];
            if (method === 'GET') {
                return mockResponse({
                    email: user.email,
                    full_name: user.full_name || 'Customer User',
                    phone_number: user.phone_number || ''
                });
            }
            if (method === 'PUT') {
                if (body.full_name !== undefined) user.full_name = body.full_name;
                if (body.phone_number !== undefined) user.phone_number = body.phone_number;
                saveStore(store);
                return mockResponse(user);
            }
        }

        // 9. USERS ALL (Admin)
        if (pathname.includes('/users/all') && method === 'GET') {
            return mockResponse(store.users);
        }

        // 10. NOTIFICATIONS
        if (pathname.includes('/users/me/notifications') && method === 'GET') {
            return mockResponse(store.customerNotifications);
        }
        if (pathname.includes('/users/admin/notifications') && method === 'GET') {
            return mockResponse(store.adminNotifications);
        }
        const notifReadMatch = pathname.match(/\/users\/notifications\/([^\/\?]+)\/read/);
        if (notifReadMatch && method === 'PUT') {
            const notifId = notifReadMatch[1];
            store.customerNotifications = store.customerNotifications.filter(n => n.id !== notifId);
            store.adminNotifications = store.adminNotifications.filter(n => n.id !== notifId);
            saveStore(store);
            return mockResponse({ success: true });
        }

        // 11. SUBSCRIPTIONS (GET /subscriptions/me)
        if (pathname.includes('/subscriptions/me') && method === 'GET') {
            const userId = currentUser ? currentUser.id : 'cust-alex-01';
            let mySub = store.subscriptions.find(s => s.customer_id === userId);
            if (!mySub) {
                mySub = {
                    id: 'sub-' + Math.random().toString(36).substring(2, 9),
                    customer_id: userId,
                    plan_id: store.plans[1] ? store.plans[1].id : 'plan-pro-2',
                    status: 'active',
                    current_period_start: new Date().toISOString(),
                    current_period_end: new Date(Date.now() + 30 * 86400000).toISOString()
                };
                store.subscriptions.push(mySub);
                saveStore(store);
            }
            return mockResponse([mySub]);
        }

        // 12. SUBSCRIPTIONS (GET /subscriptions/all)
        if (pathname.includes('/subscriptions/all') && method === 'GET') {
            return mockResponse(store.subscriptions);
        }

        // 13. SUBSCRIPTION CREATE
        if (pathname.match(/\/subscriptions\/?$/) && method === 'POST') {
            const planId = body.plan_id;
            const userId = currentUser ? currentUser.id : 'cust-alex-01';
            const sub = {
                id: 'sub-' + Math.random().toString(36).substring(2, 9),
                customer_id: userId,
                plan_id: planId,
                status: 'active',
                current_period_start: new Date().toISOString(),
                current_period_end: new Date(Date.now() + 30 * 86400000).toISOString()
            };
            store.subscriptions = store.subscriptions.filter(s => s.customer_id !== userId);
            store.subscriptions.push(sub);
            saveStore(store);
            return mockResponse(sub, 201);
        }

        // 14. SUBSCRIPTION CHANGE PLAN
        if (pathname.includes('/change_plan') && method === 'PUT') {
            let newPlanId = null;
            try {
                const u = new URL(urlStr, 'http://127.0.0.1:8000');
                newPlanId = u.searchParams.get('new_plan_id');
            } catch (e) {}
            if (!newPlanId && body.new_plan_id) newPlanId = body.new_plan_id;

            const userId = currentUser ? currentUser.id : 'cust-alex-01';
            let mySub = store.subscriptions.find(s => s.customer_id === userId);
            if (mySub && newPlanId) {
                mySub.plan_id = newPlanId;
                mySub.status = 'active';
                saveStore(store);
                return mockResponse(mySub);
            }
            return mockResponse({ detail: 'Subscription updated' });
        }

        // 15. SUBSCRIPTION PAUSE / RESUME / CANCEL
        if (pathname.includes('/pause') && method === 'PUT') {
            const userId = currentUser ? currentUser.id : 'cust-alex-01';
            let mySub = store.subscriptions.find(s => s.customer_id === userId);
            if (mySub) {
                mySub.status = 'paused';
                saveStore(store);
                return mockResponse(mySub);
            }
        }
        if (pathname.includes('/resume') && method === 'PUT') {
            const userId = currentUser ? currentUser.id : 'cust-alex-01';
            let mySub = store.subscriptions.find(s => s.customer_id === userId);
            if (mySub) {
                mySub.status = 'active';
                saveStore(store);
                return mockResponse(mySub);
            }
        }
        if (pathname.includes('/cancel') && method === 'PUT') {
            const userId = currentUser ? currentUser.id : 'cust-alex-01';
            let mySub = store.subscriptions.find(s => s.customer_id === userId);
            if (mySub) {
                mySub.status = 'cancelled';
                saveStore(store);
                return mockResponse(mySub);
            }
        }

        // 16. INVOICES (GET /invoices/me)
        if (pathname.includes('/invoices/me') && method === 'GET') {
            const userId = currentUser ? currentUser.id : 'cust-alex-01';
            const userInvoices = store.invoices.filter(inv => inv.customer_id === userId);
            return mockResponse(userInvoices);
        }

        // 17. INVOICES (GET /invoices/ all for admin)
        if (pathname.match(/\/invoices\/?$/) && method === 'GET') {
            return mockResponse(store.invoices);
        }

        // 18. INVOICE PDF DOWNLOAD
        const pdfMatch = pathname.match(/\/invoices\/([^\/\?]+)\/pdf/);
        if (pdfMatch && method === 'GET') {
            const invoiceId = pdfMatch[1];
            const inv = store.invoices.find(i => i.id === invoiceId);
            const pdfBlob = generateInvoicePdfBlob(invoiceId, inv ? inv.invoice_number : '#INV-2026', inv ? inv.amount_due : 79);
            return new Response(pdfBlob, {
                status: 200,
                headers: {
                    'Content-Type': 'application/pdf',
                    'Content-Disposition': `attachment; filename="${inv ? inv.invoice_number : 'Invoice'}.pdf"`
                }
            });
        }

        // 19. MOCK BANK CHARGE (PAYMENT)
        if (pathname.includes('/mock-bank/charge') && method === 'POST') {
            const invoiceId = body.invoice_id;
            const inv = store.invoices.find(i => i.id === invoiceId);
            if (inv) {
                inv.status = 'paid';
                inv.paid_at = new Date().toISOString();
                saveStore(store);
            }
            return mockResponse({
                status: 'success',
                message: 'Payment processed successfully',
                transaction_id: 'txn_mock_' + Date.now()
            });
        }

        // Fallback default response
        return mockResponse({ detail: 'OK' });
    }

    // Intercept Global fetch
    const originalFetch = window.fetch;
    window.fetch = async function (resource, init = {}) {
        const url = typeof resource === 'string' ? resource : (resource ? resource.url : '');

        const isApiCall =
            url.includes('127.0.0.1:8000') ||
            url.includes('localhost:8000') ||
            url.startsWith('/auth') ||
            url.startsWith('/plans') ||
            url.startsWith('/users') ||
            url.startsWith('/subscriptions') ||
            url.startsWith('/invoices') ||
            url.startsWith('/mock-bank');

        if (!isApiCall) {
            return originalFetch(resource, init);
        }

        // If on GitHub Pages, use mock API directly for instant and reliable execution
        const isStaticHost =
            window.location.hostname.endsWith('github.io') ||
            window.location.protocol === 'file:' ||
            window.location.hostname.includes('pages.dev') ||
            window.location.hostname.includes('netlify.app') ||
            window.location.hostname.includes('vercel.app');

        if (isStaticHost) {
            return handleMockApi(url, init);
        }

        // Otherwise try original fetch (local backend if running) and fallback to mock
        try {
            const res = await originalFetch(resource, init);
            return res;
        } catch (err) {
            console.warn('[BillWise] Backend not responding, switching to client-side demo backend:', err.message);
            return handleMockApi(url, init);
        }
    };

    // Quick Demo Login helper exposed globally
    window.quickDemoLogin = function (type) {
        let email = 'customer@billwise.io';
        let role = 'customer';
        let targetPage = 'dashboardcustomer.html';

        if (type === 'admin') {
            email = ADMIN_EMAIL;
            role = 'admin';
            targetPage = 'dashboardadmin.html';
        }

        const token = generateToken(email, role);
        localStorage.setItem('access_token', token);

        // Flash message & redirect
        const notice = document.createElement('div');
        notice.style.position = 'fixed';
        notice.style.top = '20px';
        notice.style.left = '50%';
        notice.style.transform = 'translateX(-50%)';
        notice.style.background = '#22C55E';
        notice.style.color = '#FFFFFF';
        notice.style.padding = '12px 24px';
        notice.style.borderRadius = '9999px';
        notice.style.fontWeight = '700';
        notice.style.boxShadow = '0 10px 25px rgba(0,0,0,0.2)';
        notice.style.zIndex = '99999';
        notice.innerText = `✨ Logged in as Demo ${type === 'admin' ? 'Admin' : 'Customer'}! Redirecting...`;
        document.body.appendChild(notice);

        setTimeout(() => {
            window.location.href = targetPage;
        }, 800);
    };

    // Auto-mount demo banner on dashboards if running statically
    document.addEventListener('DOMContentLoaded', () => {
        const isStaticHost =
            window.location.hostname.endsWith('github.io') ||
            window.location.protocol === 'file:';

        if (isStaticHost && (location.pathname.includes('dashboard') || document.querySelector('.app-container'))) {
            const banner = document.createElement('div');
            banner.id = 'demo-mode-pill';
            banner.style.position = 'fixed';
            banner.style.bottom = '18px';
            banner.style.right = '18px';
            banner.style.background = 'rgba(23, 23, 29, 0.92)';
            banner.style.border = '1px solid rgba(139, 92, 246, 0.4)';
            banner.style.color = '#e4e4e7';
            banner.style.padding = '8px 14px';
            banner.style.borderRadius = '30px';
            banner.style.fontSize = '12px';
            banner.style.fontWeight = '600';
            banner.style.display = 'flex';
            banner.style.alignItems = 'center';
            banner.style.gap = '8px';
            banner.style.boxShadow = '0 8px 24px rgba(0,0,0,0.4)';
            banner.style.zIndex = '9999';
            banner.innerHTML = `
                <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#22c55e;box-shadow:0 0 8px #22c55e;"></span>
                <span>GitHub Pages Demo Mode (Interactive Local Storage)</span>
            `;
            document.body.appendChild(banner);
        }
    });

    // Make mock utilities accessible
    window.BillWiseMockApi = {
        getStore,
        saveStore,
        generateToken
    };
})();
